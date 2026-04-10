"""Claims Database - Insurance claims records and claims management.

Stores sample claims data and provides claims lookup, filing,
and status tracking for the Claims Agent.
"""


CLAIMS = {
    "CLM-2024-001": {
        "claim_id": "CLM-2024-001",
        "policy_id": "POL-AUTO-1001",
        "customer_id": "CUST-1001",
        "type": "auto_collision",
        "status": "closed",
        "filed_date": "2024-04-12",
        "resolved_date": "2024-05-20",
        "description": "Rear-ended at stoplight on Highway 101. Minor bumper and taillight damage.",
        "amount_claimed": 4200.00,
        "amount_approved": 3200.00,
        "deductible_applied": 1000.00,
        "fault": "other_party",
        "adjuster": "Mike Thompson",
        "documents": ["police_report.pdf", "damage_photos.zip", "repair_estimate.pdf"],
    },
    "CLM-2024-002": {
        "claim_id": "CLM-2024-002",
        "policy_id": "POL-HOME-1003",
        "customer_id": "CUST-1003",
        "type": "home_water_damage",
        "status": "in_review",
        "filed_date": "2024-09-03",
        "resolved_date": None,
        "description": "Burst pipe in upstairs bathroom caused water damage to ceiling and living room flooring.",
        "amount_claimed": 18500.00,
        "amount_approved": None,
        "deductible_applied": 1000.00,
        "fault": "not_applicable",
        "adjuster": "Lisa Nguyen",
        "documents": ["damage_photos.zip", "plumber_report.pdf", "contractor_estimate.pdf"],
    },
    "CLM-2024-003": {
        "claim_id": "CLM-2024-003",
        "policy_id": "POL-AUTO-1004",
        "customer_id": "CUST-1004",
        "type": "auto_comprehensive",
        "status": "approved",
        "filed_date": "2024-07-15",
        "resolved_date": "2024-08-01",
        "description": "Hail damage during severe storm. Multiple dents on hood, roof, and trunk.",
        "amount_claimed": 6800.00,
        "amount_approved": 6700.00,
        "deductible_applied": 100.00,
        "fault": "weather_event",
        "adjuster": "Carlos Rivera",
        "documents": ["weather_report.pdf", "damage_photos.zip", "repair_estimate.pdf"],
    },
    "CLM-2024-004": {
        "claim_id": "CLM-2024-004",
        "policy_id": "POL-HEALTH-1003",
        "customer_id": "CUST-1003",
        "type": "health_emergency",
        "status": "closed",
        "filed_date": "2024-06-20",
        "resolved_date": "2024-07-15",
        "description": "Emergency room visit for chest pain. Diagnosed with anxiety-related symptoms.",
        "amount_claimed": 8900.00,
        "amount_approved": 7400.00,
        "deductible_applied": 1500.00,
        "fault": "not_applicable",
        "adjuster": "Auto-processed",
        "documents": ["er_records.pdf", "physician_notes.pdf"],
    },
    "CLM-2024-005": {
        "claim_id": "CLM-2024-005",
        "policy_id": "POL-BIZ-1004",
        "customer_id": "CUST-1004",
        "type": "business_liability",
        "status": "under_investigation",
        "filed_date": "2024-10-01",
        "resolved_date": None,
        "description": "Customer slip-and-fall incident at bakery entrance during rainy weather. Medical bills submitted.",
        "amount_claimed": 35000.00,
        "amount_approved": None,
        "deductible_applied": None,
        "fault": "pending_investigation",
        "adjuster": "Jennifer Walsh",
        "documents": ["incident_report.pdf", "witness_statements.pdf", "medical_bills.pdf", "surveillance_footage.mp4"],
    },
    "CLM-2024-006": {
        "claim_id": "CLM-2024-006",
        "policy_id": "POL-AUTO-1002",
        "customer_id": "CUST-1002",
        "type": "auto_theft",
        "status": "pending",
        "filed_date": "2024-10-15",
        "resolved_date": None,
        "description": "Vehicle broken into while parked in Manhattan. Laptop, camera, and personal items stolen.",
        "amount_claimed": 5200.00,
        "amount_approved": None,
        "deductible_applied": 500.00,
        "fault": "theft",
        "adjuster": "Pending Assignment",
        "documents": ["police_report.pdf", "items_inventory.pdf"],
    },
}


def get_claim_details(claim_id: str) -> dict:
    """Get detailed information about a specific claim.

    Args:
        claim_id: The claim identifier (e.g., CLM-2024-001).

    Returns:
        Full claim details including status, amounts, and documents.
    """
    claim = CLAIMS.get(claim_id.upper())
    if claim:
        return {"found": True, "claim": claim}
    return {"found": False, "error": f"Claim not found: {claim_id}"}


def get_customer_claims(customer_id: str) -> dict:
    """Get all claims filed by a customer.

    Args:
        customer_id: The customer identifier.

    Returns:
        List of claims with status and amounts.
    """
    claims = [c for c in CLAIMS.values() if c["customer_id"] == customer_id.upper()]
    total_claimed = sum(c["amount_claimed"] for c in claims)
    total_approved = sum(c["amount_approved"] or 0 for c in claims)

    return {
        "customer_id": customer_id,
        "claims_count": len(claims),
        "total_claimed": total_claimed,
        "total_approved": total_approved,
        "claims": claims,
    }


def get_claims_by_status(status: str) -> dict:
    """Get all claims with a specific status.

    Args:
        status: Claim status (pending, in_review, approved, under_investigation, closed).

    Returns:
        List of claims matching the status.
    """
    claims = [c for c in CLAIMS.values() if c["status"] == status.lower()]
    return {
        "status": status,
        "count": len(claims),
        "claims": claims,
    }


def file_new_claim(
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
    claim_number = f"CLM-2024-{len(CLAIMS) + 1:03d}"

    new_claim = {
        "claim_id": claim_number,
        "policy_id": policy_id.upper(),
        "customer_id": customer_id.upper(),
        "type": claim_type,
        "status": "pending",
        "filed_date": "2024-10-20",
        "resolved_date": None,
        "description": description,
        "amount_claimed": amount,
        "amount_approved": None,
        "deductible_applied": None,
        "fault": "pending_investigation",
        "adjuster": "Pending Assignment",
        "documents": [],
    }

    CLAIMS[claim_number] = new_claim

    return {
        "success": True,
        "claim_id": claim_number,
        "message": f"Claim {claim_number} filed successfully. An adjuster will be assigned within 24 hours.",
        "next_steps": [
            "Upload supporting documents via the customer portal",
            "An adjuster will contact you within 1-2 business days",
            "Keep all receipts and documentation related to the claim",
        ],
    }
