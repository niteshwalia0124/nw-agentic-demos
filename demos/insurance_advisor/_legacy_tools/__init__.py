"""Tools for the Insurance Advisor demo."""

from .claims_db import file_new_claim, get_claim_details, get_claims_by_status, get_customer_claims
from .compliance_checker import check_policy_compliance, get_state_requirements
from .customer_db import lookup_customer, search_customer_by_name
from .policy_db import compare_products, get_customer_policies, get_policy_details, get_product_catalog
from .premium_engine import calculate_premium, get_available_discounts
from .risk_calculator import calculate_risk_score, get_risk_recommendations

__all__ = [
    "lookup_customer",
    "search_customer_by_name",
    "get_product_catalog",
    "get_policy_details",
    "get_customer_policies",
    "compare_products",
    "calculate_risk_score",
    "get_risk_recommendations",
    "calculate_premium",
    "get_available_discounts",
    "get_claim_details",
    "get_customer_claims",
    "get_claims_by_status",
    "file_new_claim",
    "check_policy_compliance",
    "get_state_requirements",
]
