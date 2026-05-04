"""Risk Calculator - Computes risk scores and risk profiles for insurance underwriting.

Provides risk factor analysis used by the Risk Assessment Agent to evaluate
customers for policy recommendations and premium adjustments.
"""

from datetime import datetime


RISK_FACTORS = {
    "age": {
        "18-25": {"life": 0.8, "auto": 1.6, "health": 0.7},
        "26-35": {"life": 0.6, "auto": 1.2, "health": 0.8},
        "36-45": {"life": 0.9, "auto": 1.0, "health": 1.0},
        "46-55": {"life": 1.3, "auto": 0.9, "health": 1.3},
        "56-65": {"life": 1.8, "auto": 0.8, "health": 1.6},
        "66+": {"life": 2.5, "auto": 1.0, "health": 2.0},
    },
    "smoking": {"smoker": 2.0, "non_smoker": 1.0},
    "driving_record": {
        "clean": 0.8,
        "minor_violations": 1.2,
        "major_violations": 1.8,
        "dui": 2.5,
    },
    "credit_tier": {
        "excellent": 0.85,
        "good": 1.0,
        "fair": 1.2,
        "poor": 1.5,
    },
    "property_age_years": {
        "0-5": 0.8,
        "6-15": 1.0,
        "16-30": 1.2,
        "31+": 1.5,
    },
    "region": {
        "MH": {"auto": 1.3, "home": 1.4, "health": 1.1},
        "KA": {"auto": 1.4, "home": 1.2, "health": 1.2},
        "DL": {"auto": 1.2, "home": 1.6, "health": 1.0},
        "GJ": {"auto": 1.1, "home": 1.3, "health": 0.9},
        "default": {"auto": 1.0, "home": 1.0, "health": 1.0},
    },
}


def _get_age_bracket(age: int) -> str:
    if age <= 25:
        return "18-25"
    elif age <= 35:
        return "26-35"
    elif age <= 45:
        return "36-45"
    elif age <= 55:
        return "46-55"
    elif age <= 65:
        return "56-65"
    else:
        return "66+"


def calculate_risk_score(
    customer_age: int,
    insurance_category: str,
    state: str = "MH",
    smoking_status: str = "non_smoker",
    driving_record: str = "clean",
    credit_tier: str = "good",
    property_age_years: int = 0,
) -> dict:
    """Calculate a risk score for a customer and insurance category.

    Args:
        customer_age: Customer's age in years.
        insurance_category: Insurance type (life, auto, home, health).
        state: Indian state abbreviation for regional risk.
        smoking_status: smoker or non_smoker.
        driving_record: clean, minor_violations, major_violations, or dui.
        credit_tier: excellent, good, fair, or poor.
        property_age_years: Age of property in years (for home insurance).

    Returns:
        Risk score breakdown and overall score.
    """
    factors = {}
    category = insurance_category.lower()

    # Age factor
    age_bracket = _get_age_bracket(customer_age)
    age_data = RISK_FACTORS["age"].get(age_bracket, {})
    factors["age"] = {"bracket": age_bracket, "multiplier": age_data.get(category, 1.0)}

    # Smoking (life and health)
    if category in ("life", "health"):
        factors["smoking"] = {
            "status": smoking_status,
            "multiplier": RISK_FACTORS["smoking"].get(smoking_status, 1.0),
        }

    # Driving record (auto)
    if category == "auto":
        factors["driving_record"] = {
            "status": driving_record,
            "multiplier": RISK_FACTORS["driving_record"].get(driving_record, 1.0),
        }

    # Credit
    factors["credit"] = {
        "tier": credit_tier,
        "multiplier": RISK_FACTORS["credit_tier"].get(credit_tier, 1.0),
    }

    # Regional
    region_data = RISK_FACTORS["region"].get(state.upper(), RISK_FACTORS["region"]["default"])
    factors["region"] = {
        "state": state.upper(),
        "multiplier": region_data.get(category, 1.0),
    }

    # Property age (home)
    if category == "home" and property_age_years > 0:
        if property_age_years <= 5:
            prop_bracket = "0-5"
        elif property_age_years <= 15:
            prop_bracket = "6-15"
        elif property_age_years <= 30:
            prop_bracket = "16-30"
        else:
            prop_bracket = "31+"
        factors["property_age"] = {
            "years": property_age_years,
            "bracket": prop_bracket,
            "multiplier": RISK_FACTORS["property_age_years"][prop_bracket],
        }

    # Calculate composite score
    composite = 1.0
    for f in factors.values():
        composite *= f["multiplier"]

    # Normalize to 0-100 scale (1.0 composite = 50 risk score)
    risk_score = min(100, max(0, int(composite * 50)))

    if risk_score <= 30:
        risk_level = "low"
    elif risk_score <= 60:
        risk_level = "moderate"
    elif risk_score <= 80:
        risk_level = "high"
    else:
        risk_level = "very_high"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "composite_multiplier": round(composite, 3),
        "category": category,
        "factors": factors,
        "calculated_at": datetime.now().isoformat(),
    }


def get_risk_recommendations(risk_score: int, insurance_category: str) -> dict:
    """Get underwriting recommendations based on a risk score.

    Args:
        risk_score: The calculated risk score (0-100).
        insurance_category: The insurance category being evaluated.

    Returns:
        Underwriting recommendations and suggested actions.
    """
    category = insurance_category.lower()

    if risk_score <= 30:
        return {
            "decision": "preferred_approval",
            "premium_adjustment": -10,
            "recommendations": [
                "Eligible for preferred rates",
                "Consider bundling discounts",
                f"Recommend higher coverage limits for {category}",
            ],
        }
    elif risk_score <= 60:
        return {
            "decision": "standard_approval",
            "premium_adjustment": 0,
            "recommendations": [
                "Standard rates apply",
                f"Review {category} coverage options with customer",
                "Offer risk reduction incentives",
            ],
        }
    elif risk_score <= 80:
        return {
            "decision": "conditional_approval",
            "premium_adjustment": 25,
            "recommendations": [
                "Higher premiums required",
                "Recommend risk mitigation steps",
                "Consider higher deductible options",
                "Annual review recommended",
            ],
        }
    else:
        return {
            "decision": "manual_review",
            "premium_adjustment": 50,
            "recommendations": [
                "Requires senior underwriter review",
                "Request additional documentation",
                "Consider limited coverage options",
                "Mandatory risk assessment follow-up",
            ],
        }
