"""Claims MCP Server — backed by Cloud SQL PostgreSQL.

Exposes claims lookup, filing, and status tracking tools
via MCP protocol (Streamable HTTP transport) for deployment on Cloud Run.

Cloud SQL table:
  - claims — insurance claim records with status, amounts, documents.
"""

import os
from datetime import date

import sqlalchemy
from google.cloud.sql.connector import Connector
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

PROJECT_ID = os.getenv("GCP_PROJECT", "butterfly-987")
REGION = os.getenv("CLOUD_SQL_REGION", "us-central1")
INSTANCE_NAME = os.getenv("CLOUD_SQL_INSTANCE", "finserve-knowledge-engine-2")
DB_NAME = os.getenv("CLOUD_SQL_DB", "insurance_claims")
DB_USER = os.getenv("CLOUD_SQL_USER", "claims_user")
DB_PASS = os.getenv("CLOUD_SQL_PASS")

if not DB_PASS:
    raise RuntimeError(
        "CLOUD_SQL_PASS is required. Inject it from Secret Manager (recommended) "
        "using Cloud Run --set-secrets."
    )

INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"

# ── Database setup ──────────────────────────────────────────────────────

connector = Connector()


def getconn():
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )


engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)

# ── MCP server ──────────────────────────────────────────────────────────

mcp = FastMCP(
    name="claims-mcp",
    instructions="Insurance claims lookup, filing, and status tracking tools backed by Cloud SQL PostgreSQL.",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8080)),
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


# ── Claims Tools ────────────────────────────────────────────────────────


def _row_to_dict(row) -> dict:
    """Convert a SQLAlchemy row to a clean dict."""
    d = dict(row._mapping)
    # Convert date objects and Decimal to JSON-safe types
    for k, v in d.items():
        if isinstance(v, date):
            d[k] = v.isoformat()
        elif hasattr(v, "as_tuple"):  # Decimal
            d[k] = float(v)
    return d


@mcp.tool()
def tool_get_claim_details(claim_id: str) -> dict:
    """Get detailed information about a specific claim.

    Args:
        claim_id: The claim identifier (e.g., CLM-2024-001).

    Returns:
        Full claim details including status, amounts, and documents.
    """
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT * FROM claims WHERE claim_id = :cid"),
            {"cid": claim_id.upper()},
        )
        row = result.fetchone()
    if row:
        return {"found": True, "claim": _row_to_dict(row)}
    return {"found": False, "error": f"Claim not found: {claim_id}"}


@mcp.tool()
def tool_get_customer_claims(customer_id: str) -> dict:
    """Get all claims filed by a customer.

    Args:
        customer_id: The customer identifier.

    Returns:
        List of claims with status and amounts.
    """
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM claims WHERE customer_id = :cid ORDER BY filed_date DESC"
            ),
            {"cid": customer_id.upper()},
        )
        claims = [_row_to_dict(r) for r in result]

    total_claimed = sum(c["amount_claimed"] for c in claims)
    total_approved = sum(c["amount_approved"] or 0 for c in claims)

    return {
        "customer_id": customer_id.upper(),
        "claims_count": len(claims),
        "total_claimed": total_claimed,
        "total_approved": total_approved,
        "claims": claims,
    }


@mcp.tool()
def tool_get_claims_by_status(status: str) -> dict:
    """Get all claims with a specific status.

    Args:
        status: Claim status (pending, in_review, approved, under_investigation, closed).

    Returns:
        List of claims matching the status.
    """
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM claims WHERE status = :st ORDER BY filed_date DESC"
            ),
            {"st": status.lower()},
        )
        claims = [_row_to_dict(r) for r in result]

    return {
        "status": status,
        "count": len(claims),
        "claims": claims,
    }


@mcp.tool()
def tool_file_new_claim(
    policy_id: str,
    customer_id: str,
    claim_type: str,
    description: str,
    amount: float,
) -> dict:
    """File a new insurance claim.

    Args:
        policy_id: The policy to file the claim against.
        customer_id: The customer filing the claim.
        claim_type: Type of claim (auto_collision, auto_comprehensive, auto_theft, home_water_damage, home_fire, health_emergency, business_liability).
        description: Description of the incident.
        amount: Estimated claim amount.

    Returns:
        New claim confirmation with tracking ID.
    """
    with engine.begin() as conn:
        # Get next claim number
        result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM claims"))
        count = result.scalar()
        claim_id = f"CLM-2024-{count + 1:03d}"

        conn.execute(
            sqlalchemy.text("""
                INSERT INTO claims (claim_id, policy_id, customer_id, claim_type, status,
                    filed_date, description, amount_claimed, fault, adjuster, documents)
                VALUES (:claim_id, :policy_id, :customer_id, :claim_type, 'pending',
                    CURRENT_DATE, :description, :amount, 'pending_investigation',
                    'Pending Assignment', ARRAY[]::text[])
            """),
            {
                "claim_id": claim_id,
                "policy_id": policy_id.upper(),
                "customer_id": customer_id.upper(),
                "claim_type": claim_type,
                "description": description,
                "amount": amount,
            },
        )

    return {
        "success": True,
        "claim_id": claim_id,
        "message": f"Claim {claim_id} filed successfully. An adjuster will be assigned within 24 hours.",
        "next_steps": [
            "Upload supporting documents via the customer portal",
            "An adjuster will contact you within 1-2 business days",
            "Keep all receipts and documentation related to the claim",
        ],
    }


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
