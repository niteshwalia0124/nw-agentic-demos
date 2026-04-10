"""Customer & Policy MCP Server — backed by Firestore.

Exposes customer lookup, policy management, and product catalog tools
via MCP protocol (Streamable HTTP transport) for deployment on Cloud Run.

Firestore collections:
  - customers/{CUST-XXXX}  — customer profiles
  - policies/{POL-XXXX}    — active policies
  - products/{PRODUCT_ID}  — product catalog
"""

import os

from google.cloud import firestore
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

PROJECT_ID = os.getenv("GCP_PROJECT", "butterfly-987")
DATABASE_ID = os.getenv("FIRESTORE_DB", "insurance-advisor")

db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)

mcp = FastMCP(
    name="customer-policy-mcp",
    instructions="Customer lookup, policy management, and product catalog tools backed by Firestore.",
    host="0.0.0.0",
    port=8080,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


# ── Customer Tools ──────────────────────────────────────────────────────


@mcp.tool()
def tool_lookup_customer(customer_id: str) -> dict:
    """Look up a customer profile by customer ID.

    Args:
        customer_id: The customer identifier (e.g., CUST-1001).

    Returns:
        Full customer profile with demographics, policies, and history.
    """
    doc = db.collection("customers").document(customer_id.upper()).get()
    if doc.exists:
        return {"found": True, "customer": doc.to_dict()}
    return {"found": False, "error": f"Customer not found: {customer_id}"}


@mcp.tool()
def tool_search_customer_by_name(name: str) -> dict:
    """Search for a customer by name (partial match).

    Args:
        name: Full or partial customer name.

    Returns:
        Matching customer profiles.
    """
    matches = []
    docs = db.collection("customers").stream()
    for doc in docs:
        cust = doc.to_dict()
        if name.lower() in cust["name"].lower():
            matches.append({
                "customer_id": cust["customer_id"],
                "name": cust["name"],
                "state": cust["state"],
                "tier": cust["tier"],
                "active_policies": len(cust.get("active_policies", [])),
            })
    return {
        "query": name,
        "results_count": len(matches),
        "customers": matches,
    }


# ── Policy Tools ────────────────────────────────────────────────────────


@mcp.tool()
def tool_get_policy_details(policy_id: str) -> dict:
    """Get detailed information about an active policy.

    Args:
        policy_id: The policy identifier (e.g., POL-AUTO-1001).

    Returns:
        Full policy details including coverage and premiums.
    """
    doc = db.collection("policies").document(policy_id.upper()).get()
    if doc.exists:
        return {"found": True, "policy": doc.to_dict()}
    return {"found": False, "error": f"Policy not found: {policy_id}"}


@mcp.tool()
def tool_get_customer_policies(customer_id: str) -> dict:
    """Get all active policies for a customer.

    Args:
        customer_id: The customer identifier.

    Returns:
        List of active policies with coverage summaries.
    """
    cid = customer_id.upper()
    docs = db.collection("policies").where("customer_id", "==", cid).stream()
    policies = [d.to_dict() for d in docs]
    total_monthly = sum(p["monthly_premium"] for p in policies)

    return {
        "customer_id": cid,
        "policies_count": len(policies),
        "total_monthly_premium": total_monthly,
        "policies": policies,
    }


# ── Product Catalog Tools ──────────────────────────────────────────────


@mcp.tool()
def tool_get_product_catalog(category: str = "") -> dict:
    """Get available insurance products, optionally filtered by category.

    Args:
        category: Filter by category (life, auto, home, health, business, umbrella). Empty returns all.

    Returns:
        Available insurance products with details.
    """
    if category:
        docs = db.collection("products").where("category", "==", category.lower()).stream()
    else:
        docs = db.collection("products").stream()

    products = [d.to_dict() for d in docs]

    return {
        "filter": category or "all",
        "products_count": len(products),
        "products": products,
    }


@mcp.tool()
def tool_compare_products(product_ids: list[str]) -> dict:
    """Compare multiple insurance products side by side.

    Args:
        product_ids: List of product IDs to compare (e.g., ["AUTO_STANDARD", "AUTO_PREMIUM"]).

    Returns:
        Side-by-side comparison of selected products.
    """
    products = []
    for pid in product_ids:
        doc = db.collection("products").document(pid.upper()).get()
        if doc.exists:
            products.append(doc.to_dict())

    return {
        "comparison_count": len(products),
        "products": products,
    }


# ── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
