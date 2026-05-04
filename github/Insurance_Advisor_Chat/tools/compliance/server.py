"""Compliance MCP Server — backed by BigQuery.

Exposes regulatory compliance validation tools via MCP protocol
(Streamable HTTP transport) for deployment on Cloud Run.

BigQuery tables:
  - insurance_compliance.state_regulations   — per-state rules
  - insurance_compliance.federal_regulations — federal requirements
"""

import os

from google.cloud import bigquery
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

PROJECT_ID = os.getenv("GCP_PROJECT", "YOUR_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET", "insurance_compliance")

bq_client = bigquery.Client(project=PROJECT_ID)

mcp = FastMCP(
    name="compliance-mcp",
    instructions="Insurance regulatory compliance validation tools backed by BigQuery.",
    host="0.0.0.0",
    port=8080,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


# ── Helpers ─────────────────────────────────────────────────────────────


def _query_state(state_code: str) -> dict | None:
    """Fetch state regulations from BigQuery."""
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.state_regulations`
        WHERE state_code = @state
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("state", "STRING", state_code.upper()),
        ]
    )
    results = bq_client.query(query, job_config=job_config).result()
    rows = [dict(row) for row in results]
    return rows[0] if rows else None


def _query_federal(category: str = "") -> list[dict]:
    """Fetch applicable federal regulations from BigQuery."""
    if category:
        query = f"""
            SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.federal_regulations`
            WHERE ARRAY_LENGTH(applies_to) = 0
               OR @cat IN UNNEST(applies_to)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("cat", "STRING", category.lower()),
            ]
        )
    else:
        query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.federal_regulations`"
        job_config = None

    results = bq_client.query(query, job_config=job_config).result()
    return [dict(row) for row in results]


# ── Compliance Tools ────────────────────────────────────────────────────


@mcp.tool()
def tool_check_policy_compliance(
    state: str,
    insurance_category: str,
    coverage_details: str,
    premium_change_pct: float = 0,
) -> dict:
    """Check if a policy meets state and federal compliance requirements.

    Args:
        state: Indian state abbreviation (e.g., MH, KA, DL, GJ).
        insurance_category: Insurance type (auto, home, life, health, business).
        coverage_details: Description of the coverage being offered.
        premium_change_pct: Percentage change in premium from previous period.

    Returns:
        Compliance check results with any violations or warnings.
    """
    category = insurance_category.lower()
    state_upper = state.upper()
    state_regs = _query_state(state_upper)

    violations = []
    warnings = []
    compliant_items = []

    if state_regs:
        # Check rate increase cap
        if premium_change_pct > 0:
            cap = state_regs.get("rate_increase_cap_pct", 25)
            if premium_change_pct > cap:
                violations.append({
                    "rule": "rate_increase_cap",
                    "detail": f"Premium increase of {premium_change_pct}% exceeds {state_upper} cap of {cap}%",
                    "severity": "high",
                })
            else:
                compliant_items.append(f"Premium increase within {state_upper} {cap}% cap")

        # Check state-specific requirements
        req_coverages = state_regs.get("required_coverages", [])
        if req_coverages and category == "auto":
            warnings.append({
                "rule": "required_coverages",
                "detail": f"{state_upper} requires: {', '.join(req_coverages)}",
                "severity": "medium",
            })

        if state_regs.get("hurricane_moratorium") and category == "home":
            warnings.append({
                "rule": "hurricane_moratorium",
                "detail": f"{state_upper} may have active hurricane moratorium periods affecting policy changes",
                "severity": "medium",
            })

        if state_regs.get("sinkhole_coverage_required") and category == "home":
            warnings.append({
                "rule": "sinkhole_coverage",
                "detail": f"{state_upper} requires sinkhole coverage disclosure and availability",
                "severity": "medium",
            })

        # Data privacy
        privacy_reg = state_regs.get("data_privacy", "standard_state")
        compliant_items.append(f"Subject to {privacy_reg} data privacy requirements")

        # Discrimination rules
        disc_prohibited = state_regs.get("discrimination_prohibited", [])
        if disc_prohibited:
            compliant_items.append(f"Prohibited factors: {', '.join(disc_prohibited)}")

    else:
        warnings.append({
            "rule": "state_regulations",
            "detail": f"No specific regulations on file for {state_upper}. Apply standard federal guidelines.",
            "severity": "low",
        })

    # Federal compliance
    federal_regs = _query_federal(category)
    for reg in federal_regs:
        compliant_items.append(f"{reg['name']}: applicable")

    is_compliant = len(violations) == 0

    return {
        "compliant": is_compliant,
        "state": state_upper,
        "category": category,
        "violations": violations,
        "warnings": warnings,
        "compliant_items": compliant_items,
        "regulatory_body": state_regs["department"] if state_regs else "State Insurance Department",
    }


@mcp.tool()
def tool_get_state_requirements(state: str) -> dict:
    """Get all regulatory requirements for a specific state.

    Args:
        state: Indian state abbreviation (e.g., MH, KA, DL, GJ).

    Returns:
        State regulations and applicable federal regulations.
    """
    state_upper = state.upper()
    state_regs = _query_state(state_upper)

    if not state_regs:
        return {
            "found": False,
            "error": f"No regulations on file for {state_upper}. Contact compliance team.",
        }

    federal_regs = _query_federal()

    return {
        "found": True,
        "state_regulations": state_regs,
        "federal_regulations": federal_regs,
    }


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
