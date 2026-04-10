"""Compliance Checker - Regulatory compliance validation for insurance operations.

Validates policies, claims, and recommendations against state and federal
regulatory requirements for the Compliance Agent.
"""


STATE_REGULATIONS = {
    "CA": {
        "state": "California",
        "department": "California Department of Insurance",
        "rules": {
            "auto_minimum_liability": {"bodily_injury": "15/30", "property_damage": 5000},
            "rate_increase_cap_pct": 15,
            "cancellation_notice_days": 20,
            "claims_response_days": 15,
            "discrimination_prohibited": ["credit_score_auto", "gender_auto"],
            "required_discounts": ["good_driver", "good_student", "multi_vehicle"],
            "data_privacy": "CCPA",
        },
    },
    "NY": {
        "state": "New York",
        "department": "New York Department of Financial Services",
        "rules": {
            "auto_minimum_liability": {"bodily_injury": "25/50", "property_damage": 10000},
            "rate_increase_cap_pct": 20,
            "cancellation_notice_days": 15,
            "claims_response_days": 30,
            "discrimination_prohibited": ["credit_score_all"],
            "required_coverages": ["uninsured_motorist", "personal_injury_protection"],
            "data_privacy": "NY_SHIELD_Act",
        },
    },
    "FL": {
        "state": "Florida",
        "department": "Florida Office of Insurance Regulation",
        "rules": {
            "auto_minimum_liability": {"bodily_injury": "25/50", "property_damage": 10000},
            "rate_increase_cap_pct": 25,
            "cancellation_notice_days": 10,
            "claims_response_days": 14,
            "hurricane_moratorium": True,
            "sinkhole_coverage_required": True,
            "data_privacy": "FIPA",
        },
    },
    "TX": {
        "state": "Texas",
        "department": "Texas Department of Insurance",
        "rules": {
            "auto_minimum_liability": {"bodily_injury": "30/60", "property_damage": 25000},
            "rate_increase_cap_pct": 20,
            "cancellation_notice_days": 10,
            "claims_response_days": 15,
            "hail_damage_provisions": True,
            "data_privacy": "standard_state",
        },
    },
}

FEDERAL_REGULATIONS = {
    "fair_lending": {
        "name": "Fair Credit Reporting Act (FCRA)",
        "requirements": [
            "Adverse action notices required when credit affects premium",
            "Consumer right to dispute credit-based decisions",
            "Annual free credit report access",
        ],
    },
    "hipaa": {
        "name": "HIPAA",
        "requirements": [
            "Protected health information must be secured",
            "Minimum necessary standard for health data access",
            "Breach notification within 60 days",
        ],
        "applies_to": ["health"],
    },
    "ada": {
        "name": "Americans with Disabilities Act",
        "requirements": [
            "Cannot discriminate based on disability in underwriting",
            "Reasonable accommodations in service delivery",
        ],
    },
    "flood_insurance": {
        "name": "National Flood Insurance Program (NFIP)",
        "requirements": [
            "Federally-backed flood insurance available in participating communities",
            "Mandatory for properties in high-risk flood zones with federal mortgages",
        ],
        "applies_to": ["home"],
    },
}


def check_policy_compliance(
    state: str,
    insurance_category: str,
    coverage_details: str,
    premium_change_pct: float = 0,
) -> dict:
    """Check if a policy meets state and federal compliance requirements.

    Args:
        state: US state abbreviation.
        insurance_category: Insurance type (auto, home, life, health, business).
        coverage_details: JSON string describing the coverage being offered.
        premium_change_pct: Percentage change in premium from previous period.

    Returns:
        Compliance check results with any violations or warnings.
    """
    category = insurance_category.lower()
    state_upper = state.upper()
    state_regs = STATE_REGULATIONS.get(state_upper, None)

    violations = []
    warnings = []
    compliant_items = []

    if state_regs:
        rules = state_regs["rules"]

        # Check rate increase cap
        if premium_change_pct > 0:
            cap = rules.get("rate_increase_cap_pct", 25)
            if premium_change_pct > cap:
                violations.append({
                    "rule": "rate_increase_cap",
                    "detail": f"Premium increase of {premium_change_pct}% exceeds {state_upper} cap of {cap}%",
                    "severity": "high",
                })
            else:
                compliant_items.append(f"Premium increase within {state_upper} {cap}% cap")

        # Check state-specific requirements
        if "required_coverages" in rules and category == "auto":
            warnings.append({
                "rule": "required_coverages",
                "detail": f"{state_upper} requires: {', '.join(rules['required_coverages'])}",
                "severity": "medium",
            })

        if rules.get("hurricane_moratorium") and category == "home":
            warnings.append({
                "rule": "hurricane_moratorium",
                "detail": f"{state_upper} may have active hurricane moratorium periods affecting policy changes",
                "severity": "medium",
            })

        if rules.get("sinkhole_coverage_required") and category == "home":
            warnings.append({
                "rule": "sinkhole_coverage",
                "detail": f"{state_upper} requires sinkhole coverage disclosure and availability",
                "severity": "medium",
            })

        # Data privacy
        privacy_reg = rules.get("data_privacy", "standard_state")
        compliant_items.append(f"Subject to {privacy_reg} data privacy requirements")

        # Discrimination rules
        if "discrimination_prohibited" in rules:
            compliant_items.append(f"Prohibited factors: {', '.join(rules['discrimination_prohibited'])}")

    else:
        warnings.append({
            "rule": "state_regulations",
            "detail": f"No specific regulations on file for {state_upper}. Apply standard federal guidelines.",
            "severity": "low",
        })

    # Federal compliance
    for reg_id, reg in FEDERAL_REGULATIONS.items():
        if "applies_to" in reg and category not in reg["applies_to"]:
            continue
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


def get_state_requirements(state: str) -> dict:
    """Get all regulatory requirements for a specific state.

    Args:
        state: US state abbreviation.

    Returns:
        State regulations and applicable federal regulations.
    """
    state_upper = state.upper()
    state_regs = STATE_REGULATIONS.get(state_upper, None)

    if not state_regs:
        return {
            "found": False,
            "error": f"No regulations on file for {state_upper}. Contact compliance team.",
        }

    return {
        "found": True,
        "state_regulations": state_regs,
        "federal_regulations": FEDERAL_REGULATIONS,
    }
