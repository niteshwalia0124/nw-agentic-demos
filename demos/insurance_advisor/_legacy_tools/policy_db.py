"""Policy Database - Insurance product catalog and active policy store.

Provides policy product lookup, coverage comparison, and active policy
management for the Insurance Advisor multi-agent system.
"""


PRODUCTS_CATALOG = {
    "TERM_LIFE": {
        "product_id": "TERM_LIFE",
        "name": "SecureLife Term",
        "category": "life",
        "description": "Affordable term life insurance with fixed premiums for 10, 20, or 30 years",
        "coverage_range": {"min": 100000, "max": 2000000},
        "term_options_years": [10, 20, 30],
        "base_monthly_premium": 25.00,
        "features": ["Level premiums", "Convertible to whole life", "Accelerated death benefit"],
        "eligibility": {"min_age": 18, "max_age": 65},
    },
    "WHOLE_LIFE": {
        "product_id": "WHOLE_LIFE",
        "name": "SecureLife Permanent",
        "category": "life",
        "description": "Permanent life insurance with cash value accumulation",
        "coverage_range": {"min": 50000, "max": 5000000},
        "term_options_years": ["lifetime"],
        "base_monthly_premium": 120.00,
        "features": ["Cash value growth", "Guaranteed death benefit", "Policy loans available", "Dividend eligible"],
        "eligibility": {"min_age": 18, "max_age": 70},
    },
    "AUTO_STANDARD": {
        "product_id": "AUTO_STANDARD",
        "name": "DriveShield Standard",
        "category": "auto",
        "description": "Comprehensive auto insurance with liability, collision, and uninsured motorist coverage",
        "coverage_options": {
            "liability": {"bodily_injury": "100/300", "property_damage": 100000},
            "collision_deductible": [500, 1000, 2000],
            "comprehensive_deductible": [250, 500, 1000],
        },
        "base_monthly_premium": 95.00,
        "features": ["Roadside assistance", "Rental car reimbursement", "Accident forgiveness"],
        "eligibility": {"min_age": 16, "max_age": 99},
    },
    "AUTO_PREMIUM": {
        "product_id": "AUTO_PREMIUM",
        "name": "DriveShield Premium",
        "category": "auto",
        "description": "Premium auto coverage with gap insurance, new car replacement, and vanishing deductible",
        "coverage_options": {
            "liability": {"bodily_injury": "250/500", "property_damage": 250000},
            "collision_deductible": [250, 500],
            "comprehensive_deductible": [100, 250],
        },
        "base_monthly_premium": 165.00,
        "features": ["Gap insurance", "New car replacement", "Vanishing deductible", "Diminishing deductible"],
        "eligibility": {"min_age": 18, "max_age": 99},
    },
    "HOME_STANDARD": {
        "product_id": "HOME_STANDARD",
        "name": "HomeGuard Standard",
        "category": "home",
        "description": "Standard homeowners insurance covering dwelling, personal property, and liability",
        "coverage_options": {
            "dwelling": {"min": 150000, "max": 1000000},
            "personal_property": "50% of dwelling",
            "liability": 300000,
            "deductible": [1000, 2500, 5000],
        },
        "base_monthly_premium": 110.00,
        "features": ["Replacement cost coverage", "Additional living expenses", "Identity theft protection"],
        "eligibility": {"property_types": ["single_family", "condo", "townhouse"]},
    },
    "HEALTH_PPO": {
        "product_id": "HEALTH_PPO",
        "name": "HealthFirst PPO",
        "category": "health",
        "description": "Flexible PPO health plan with wide provider network",
        "coverage_options": {
            "deductible": [1500, 3000, 5000],
            "out_of_pocket_max": [6000, 8000, 12000],
            "copay_primary": 30,
            "copay_specialist": 50,
        },
        "base_monthly_premium": 450.00,
        "features": ["No referral needed for specialists", "Out-of-network coverage", "Preventive care 100%"],
        "eligibility": {"min_age": 0, "max_age": 64},
    },
    "BUSINESS_LIABILITY": {
        "product_id": "BUSINESS_LIABILITY",
        "name": "BizShield General Liability",
        "category": "business",
        "description": "General liability for small to mid-size businesses",
        "coverage_options": {
            "per_occurrence": [1000000, 2000000],
            "aggregate": [2000000, 4000000],
            "products_completed_ops": True,
        },
        "base_monthly_premium": 85.00,
        "features": ["Product liability", "Completed operations", "Personal & advertising injury", "Medical payments"],
        "eligibility": {"business_types": ["retail", "food_service", "professional_services", "construction"]},
    },
    "UMBRELLA": {
        "product_id": "UMBRELLA",
        "name": "UltraShield Umbrella",
        "category": "umbrella",
        "description": "Additional liability coverage above existing auto, home, or business policies",
        "coverage_range": {"min": 1000000, "max": 10000000},
        "base_monthly_premium": 30.00,
        "features": ["Extends auto liability", "Extends home liability", "Worldwide coverage", "Legal defense costs"],
        "eligibility": {"requires_underlying": ["auto", "home"]},
    },
}


ACTIVE_POLICIES = {
    "POL-AUTO-1001": {
        "policy_id": "POL-AUTO-1001",
        "customer_id": "CUST-1001",
        "product_id": "AUTO_STANDARD",
        "product_name": "DriveShield Standard",
        "status": "active",
        "effective_date": "2024-01-15",
        "expiration_date": "2025-01-15",
        "monthly_premium": 112.00,
        "coverage_summary": {"liability": "100/300", "collision_deductible": 1000, "comprehensive_deductible": 500},
        "vehicle": {"year": 2022, "make": "Toyota", "model": "Camry", "vin": "1HGBH41JXMN109186"},
    },
    "POL-HOME-1001": {
        "policy_id": "POL-HOME-1001",
        "customer_id": "CUST-1001",
        "product_id": "HOME_STANDARD",
        "product_name": "HomeGuard Standard",
        "status": "active",
        "effective_date": "2023-06-01",
        "expiration_date": "2024-06-01",
        "monthly_premium": 135.00,
        "coverage_summary": {"dwelling": 650000, "personal_property": 325000, "liability": 300000, "deductible": 2500},
    },
    "POL-AUTO-1002": {
        "policy_id": "POL-AUTO-1002",
        "customer_id": "CUST-1002",
        "product_id": "AUTO_STANDARD",
        "product_name": "DriveShield Standard",
        "status": "active",
        "effective_date": "2024-03-01",
        "expiration_date": "2025-03-01",
        "monthly_premium": 138.00,
        "coverage_summary": {"liability": "100/300", "collision_deductible": 500, "comprehensive_deductible": 250},
    },
    "POL-HOME-1003": {
        "policy_id": "POL-HOME-1003",
        "customer_id": "CUST-1003",
        "product_id": "HOME_STANDARD",
        "product_name": "HomeGuard Standard",
        "status": "active",
        "effective_date": "2023-01-01",
        "expiration_date": "2024-01-01",
        "monthly_premium": 98.00,
        "coverage_summary": {"dwelling": 420000, "personal_property": 210000, "liability": 300000, "deductible": 1000},
    },
    "POL-LIFE-1003": {
        "policy_id": "POL-LIFE-1003",
        "customer_id": "CUST-1003",
        "product_id": "WHOLE_LIFE",
        "product_name": "SecureLife Permanent",
        "status": "active",
        "effective_date": "2015-11-20",
        "expiration_date": "lifetime",
        "monthly_premium": 285.00,
        "coverage_summary": {"death_benefit": 500000, "cash_value": 87500},
    },
    "POL-HEALTH-1003": {
        "policy_id": "POL-HEALTH-1003",
        "customer_id": "CUST-1003",
        "product_id": "HEALTH_PPO",
        "product_name": "HealthFirst PPO",
        "status": "active",
        "effective_date": "2024-01-01",
        "expiration_date": "2024-12-31",
        "monthly_premium": 520.00,
        "coverage_summary": {"deductible": 1500, "out_of_pocket_max": 6000},
    },
    "POL-BIZ-1004": {
        "policy_id": "POL-BIZ-1004",
        "customer_id": "CUST-1004",
        "product_id": "BUSINESS_LIABILITY",
        "product_name": "BizShield General Liability",
        "status": "active",
        "effective_date": "2024-02-01",
        "expiration_date": "2025-02-01",
        "monthly_premium": 145.00,
        "coverage_summary": {"per_occurrence": 1000000, "aggregate": 2000000},
        "business": {"name": "Martinez Bakery & Cafe", "type": "food_service", "employees": 12},
    },
    "POL-AUTO-1004": {
        "policy_id": "POL-AUTO-1004",
        "customer_id": "CUST-1004",
        "product_id": "AUTO_PREMIUM",
        "product_name": "DriveShield Premium",
        "status": "active",
        "effective_date": "2024-05-01",
        "expiration_date": "2025-05-01",
        "monthly_premium": 178.00,
        "coverage_summary": {"liability": "250/500", "collision_deductible": 250, "comprehensive_deductible": 100},
    },
    "POL-HOME-1004": {
        "policy_id": "POL-HOME-1004",
        "customer_id": "CUST-1004",
        "product_id": "HOME_STANDARD",
        "product_name": "HomeGuard Standard",
        "status": "active",
        "effective_date": "2024-01-15",
        "expiration_date": "2025-01-15",
        "monthly_premium": 195.00,
        "coverage_summary": {"dwelling": 850000, "personal_property": 425000, "liability": 300000, "deductible": 2500},
    },
}


def get_product_catalog(category: str = "") -> dict:
    """Get available insurance products, optionally filtered by category.

    Args:
        category: Filter by category (life, auto, home, health, business, umbrella). Empty returns all.

    Returns:
        Available insurance products with details.
    """
    if category:
        products = {k: v for k, v in PRODUCTS_CATALOG.items() if v["category"] == category.lower()}
    else:
        products = PRODUCTS_CATALOG

    return {
        "filter": category or "all",
        "products_count": len(products),
        "products": list(products.values()),
    }


def get_policy_details(policy_id: str) -> dict:
    """Get detailed information about an active policy.

    Args:
        policy_id: The policy identifier (e.g., POL-AUTO-1001).

    Returns:
        Full policy details including coverage and premiums.
    """
    policy = ACTIVE_POLICIES.get(policy_id.upper())
    if policy:
        return {"found": True, "policy": policy}
    return {"found": False, "error": f"Policy not found: {policy_id}"}


def get_customer_policies(customer_id: str) -> dict:
    """Get all active policies for a customer.

    Args:
        customer_id: The customer identifier.

    Returns:
        List of active policies with coverage summaries.
    """
    policies = [p for p in ACTIVE_POLICIES.values() if p["customer_id"] == customer_id.upper()]
    total_monthly = sum(p["monthly_premium"] for p in policies)

    return {
        "customer_id": customer_id,
        "policies_count": len(policies),
        "total_monthly_premium": total_monthly,
        "policies": policies,
    }


def compare_products(product_ids: list[str]) -> dict:
    """Compare multiple insurance products side by side.

    Args:
        product_ids: List of product IDs to compare (e.g., ["AUTO_STANDARD", "AUTO_PREMIUM"]).

    Returns:
        Side-by-side comparison of selected products.
    """
    products = []
    for pid in product_ids:
        product = PRODUCTS_CATALOG.get(pid.upper())
        if product:
            products.append(product)

    return {
        "comparison_count": len(products),
        "products": products,
    }
