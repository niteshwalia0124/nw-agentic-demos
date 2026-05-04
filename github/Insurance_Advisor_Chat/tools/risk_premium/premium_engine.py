"""Premium Engine - Calculates insurance premiums with discounts and adjustments.

Computes monthly and annual premiums based on product base rates,
risk multipliers, coverage selections, and applicable discounts.
"""


DISCOUNT_RULES = {
    "multi_policy": {"discount_pct": 12, "description": "Multi-policy bundle discount", "min_policies": 2},
    "loyalty_5yr": {"discount_pct": 8, "description": "5+ year loyalty discount", "min_years": 5},
    "loyalty_10yr": {"discount_pct": 15, "description": "10+ year loyalty discount", "min_years": 10},
    "safe_driver": {"discount_pct": 10, "description": "Clean driving record discount"},
    "non_smoker": {"discount_pct": 15, "description": "Non-smoker discount", "categories": ["life", "health"]},
    "home_security": {"discount_pct": 5, "description": "Home security system discount", "categories": ["home"]},
    "good_credit": {"discount_pct": 7, "description": "Good credit discount"},
    "annual_pay": {"discount_pct": 5, "description": "Annual payment discount"},
    "paperless": {"discount_pct": 3, "description": "Paperless billing discount"},
}


COVERAGE_MULTIPLIERS = {
    "auto": {
        "deductible_250": 1.25,
        "deductible_500": 1.10,
        "deductible_1000": 1.00,
        "deductible_2000": 0.85,
    },
    "home": {
        "deductible_1000": 1.15,
        "deductible_2500": 1.00,
        "deductible_5000": 0.85,
    },
    "health": {
        "deductible_1500": 1.30,
        "deductible_3000": 1.00,
        "deductible_5000": 0.75,
    },
}


def calculate_premium(
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
    # Determine category from product_id
    pid = product_id.upper()
    if "AUTO" in pid:
        category = "auto"
    elif "HOME" in pid:
        category = "home"
    elif "LIFE" in pid or "WHOLE" in pid or "TERM" in pid:
        category = "life"
    elif "HEALTH" in pid:
        category = "health"
    elif "BIZ" in pid or "BUSINESS" in pid:
        category = "business"
    elif "UMBRELLA" in pid:
        category = "umbrella"
    else:
        category = "other"

    # Start with risk-adjusted base
    risk_adjusted = base_monthly_premium * risk_multiplier

    # Coverage level adjustment
    coverage_adj = {"standard": 1.0, "enhanced": 1.15, "premium": 1.35}.get(coverage_level, 1.0)
    coverage_adjusted = risk_adjusted * coverage_adj

    # Deductible adjustment
    deductible_key = f"deductible_{deductible}"
    cat_multipliers = COVERAGE_MULTIPLIERS.get(category, {})
    deductible_mult = cat_multipliers.get(deductible_key, 1.0)
    deductible_adjusted = coverage_adjusted * deductible_mult

    # Calculate discounts
    applied_discounts = []
    total_discount_pct = 0

    # Auto-apply multi-policy
    if existing_policy_count >= 2:
        rule = DISCOUNT_RULES["multi_policy"]
        applied_discounts.append({"code": "multi_policy", "description": rule["description"], "pct": rule["discount_pct"]})
        total_discount_pct += rule["discount_pct"]

    # Auto-apply loyalty
    if customer_tenure_years >= 10:
        rule = DISCOUNT_RULES["loyalty_10yr"]
        applied_discounts.append({"code": "loyalty_10yr", "description": rule["description"], "pct": rule["discount_pct"]})
        total_discount_pct += rule["discount_pct"]
    elif customer_tenure_years >= 5:
        rule = DISCOUNT_RULES["loyalty_5yr"]
        applied_discounts.append({"code": "loyalty_5yr", "description": rule["description"], "pct": rule["discount_pct"]})
        total_discount_pct += rule["discount_pct"]

    # Apply requested discounts
    for code in apply_discounts:
        if code in DISCOUNT_RULES and code not in ("multi_policy", "loyalty_5yr", "loyalty_10yr"):
            rule = DISCOUNT_RULES[code]
            # Check category restrictions
            if "categories" in rule and category not in rule["categories"]:
                continue
            applied_discounts.append({"code": code, "description": rule["description"], "pct": rule["discount_pct"]})
            total_discount_pct += rule["discount_pct"]

    # Cap total discount at 35%
    total_discount_pct = min(35, total_discount_pct)
    discount_amount = deductible_adjusted * (total_discount_pct / 100)
    final_monthly = round(deductible_adjusted - discount_amount, 2)

    return {
        "product_id": pid,
        "category": category,
        "premium_breakdown": {
            "base_monthly": base_monthly_premium,
            "risk_multiplier": round(risk_multiplier, 3),
            "risk_adjusted": round(risk_adjusted, 2),
            "coverage_level": coverage_level,
            "coverage_adjustment": coverage_adj,
            "deductible": deductible,
            "deductible_multiplier": deductible_mult,
            "pre_discount_monthly": round(deductible_adjusted, 2),
        },
        "discounts": {
            "applied": applied_discounts,
            "total_discount_pct": total_discount_pct,
            "discount_amount": round(discount_amount, 2),
        },
        "final_premium": {
            "monthly": final_monthly,
            "quarterly": round(final_monthly * 3, 2),
            "semi_annual": round(final_monthly * 6, 2),
            "annual": round(final_monthly * 12, 2),
        },
    }


def get_available_discounts(category: str, existing_policy_count: int = 0, customer_tenure_years: int = 0) -> dict:
    """List all discounts available for a given insurance category.

    Args:
        category: Insurance category (auto, home, life, health, business).
        existing_policy_count: Number of existing policies held.
        customer_tenure_years: Customer tenure in years.

    Returns:
        Available and auto-applied discounts.
    """
    available = []
    auto_applied = []

    for code, rule in DISCOUNT_RULES.items():
        if "categories" in rule and category.lower() not in rule["categories"]:
            continue

        entry = {"code": code, "description": rule["description"], "discount_pct": rule["discount_pct"]}

        if code == "multi_policy" and existing_policy_count >= 2:
            auto_applied.append(entry)
        elif code == "loyalty_10yr" and customer_tenure_years >= 10:
            auto_applied.append(entry)
        elif code == "loyalty_5yr" and 5 <= customer_tenure_years < 10:
            auto_applied.append(entry)
        else:
            available.append(entry)

    return {
        "category": category,
        "auto_applied": auto_applied,
        "available_discounts": available,
    }
