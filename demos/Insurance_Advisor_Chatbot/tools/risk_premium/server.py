"""Risk & Premium MCP Server.

Exposes risk scoring and premium calculation tools via MCP protocol
(Streamable HTTP transport) for deployment on Cloud Run.

Local usage:
    python server.py

Then connect from ADK with:
    McpToolset.from_server(SseServerParams(url="http://localhost:8080/mcp"))
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from risk_calculator import (
    calculate_risk_score,
    get_risk_recommendations,
)
from premium_engine import (
    calculate_premium,
    get_available_discounts,
)

mcp = FastMCP(
    name="risk-premium-mcp",
    instructions="Risk scoring and premium calculation tools for insurance underwriting.",
    host="0.0.0.0",
    port=8080,
    # Disable DNS rebinding protection — Cloud Run handles security via IAM
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


# ── Risk Calculator Tools ──────────────────────────────────────────────


@mcp.tool()
def tool_calculate_risk_score(
    customer_age: int,
    insurance_category: str,
    state: str = "CA",
    smoking_status: str = "non_smoker",
    driving_record: str = "clean",
    credit_tier: str = "good",
    property_age_years: int = 0,
) -> dict:
    """Calculate a risk score for a customer and insurance category.

    Args:
        customer_age: Customer's age in years.
        insurance_category: Insurance type (life, auto, home, health).
        state: US state abbreviation for regional risk.
        smoking_status: smoker or non_smoker.
        driving_record: clean, minor_violations, major_violations, or dui.
        credit_tier: excellent, good, fair, or poor.
        property_age_years: Age of property in years (for home insurance).

    Returns:
        Risk score breakdown and overall score.
    """
    return calculate_risk_score(
        customer_age=customer_age,
        insurance_category=insurance_category,
        state=state,
        smoking_status=smoking_status,
        driving_record=driving_record,
        credit_tier=credit_tier,
        property_age_years=property_age_years,
    )


@mcp.tool()
def tool_get_risk_recommendations(risk_score: int, insurance_category: str) -> dict:
    """Get underwriting recommendations based on a risk score.

    Args:
        risk_score: The calculated risk score (0-100).
        insurance_category: The insurance category being evaluated.

    Returns:
        Underwriting recommendations and suggested actions.
    """
    return get_risk_recommendations(risk_score, insurance_category)


# ── Premium Engine Tools ───────────────────────────────────────────────


@mcp.tool()
def tool_calculate_premium(
    product_id: str,
    base_monthly_premium: float,
    risk_multiplier: float,
    coverage_level: str = "standard",
    deductible: int = 1000,
    existing_policy_count: int = 0,
    customer_tenure_years: int = 0,
    apply_discounts: list[str] = [],
) -> dict:
    """Calculate the final premium for a policy.

    Args:
        product_id: The insurance product ID (e.g., AUTO_STANDARD).
        base_monthly_premium: Base premium from product catalog.
        risk_multiplier: Risk composite multiplier from risk calculator.
        coverage_level: standard, enhanced, or premium tier.
        deductible: Selected deductible amount.
        existing_policy_count: Number of other active policies (for bundling).
        customer_tenure_years: Years as a customer (for loyalty).
        apply_discounts: List of applicable discount codes (safe_driver, non_smoker, etc.).

    Returns:
        Premium breakdown with base, adjustments, discounts, and final amount.
    """
    return calculate_premium(
        product_id=product_id,
        base_monthly_premium=base_monthly_premium,
        risk_multiplier=risk_multiplier,
        coverage_level=coverage_level,
        deductible=deductible,
        existing_policy_count=existing_policy_count,
        customer_tenure_years=customer_tenure_years,
        apply_discounts=apply_discounts,
    )


@mcp.tool()
def tool_get_available_discounts(
    category: str,
    existing_policy_count: int = 0,
    customer_tenure_years: int = 0,
) -> dict:
    """List all discounts available for a given insurance category.

    Args:
        category: Insurance category (auto, home, life, health, business).
        existing_policy_count: Number of existing policies held.
        customer_tenure_years: Customer tenure in years.

    Returns:
        Available and auto-applied discounts.
    """
    return get_available_discounts(
        category=category,
        existing_policy_count=existing_policy_count,
        customer_tenure_years=customer_tenure_years,
    )


if __name__ == "__main__":
    import uvicorn

    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)
