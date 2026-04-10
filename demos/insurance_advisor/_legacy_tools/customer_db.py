"""Customer Database - Simulated enterprise customer data store.

Provides customer profile lookup, policy history, and account management
for the Insurance Advisor multi-agent system.
"""


CUSTOMERS_DB = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "name": "Rajesh Sharma",
        "age": 35,
        "gender": "male",
        "marital_status": "married",
        "dependents": 2,
        "occupation": "software_engineer",
        "annual_income": 185000,
        "state": "California",
        "city": "San Jose",
        "credit_score": 780,
        "smoking_status": "non_smoker",
        "health_conditions": [],
        "driving_record": {"violations": 0, "accidents": 0, "years_licensed": 13},
        "active_policies": ["POL-AUTO-1001", "POL-HOME-1001"],
        "claims_history": ["CLM-2024-001"],
        "customer_since": "2019-03-15",
        "tier": "Gold",
    },
    "CUST-1002": {
        "customer_id": "CUST-1002",
        "name": "Emily Chen",
        "age": 28,
        "gender": "female",
        "marital_status": "single",
        "dependents": 0,
        "occupation": "marketing_manager",
        "annual_income": 95000,
        "state": "New York",
        "city": "Brooklyn",
        "credit_score": 720,
        "smoking_status": "non_smoker",
        "health_conditions": [],
        "driving_record": {"violations": 1, "accidents": 0, "years_licensed": 8},
        "active_policies": ["POL-AUTO-1002"],
        "claims_history": [],
        "customer_since": "2022-07-01",
        "tier": "Silver",
    },
    "CUST-1003": {
        "customer_id": "CUST-1003",
        "name": "Robert Williams",
        "age": 62,
        "gender": "male",
        "marital_status": "married",
        "dependents": 0,
        "occupation": "retired",
        "annual_income": 75000,
        "state": "Florida",
        "city": "Tampa",
        "credit_score": 810,
        "smoking_status": "former_smoker",
        "health_conditions": ["hypertension"],
        "driving_record": {"violations": 0, "accidents": 1, "years_licensed": 44},
        "active_policies": ["POL-HOME-1003", "POL-LIFE-1003", "POL-HEALTH-1003"],
        "claims_history": ["CLM-2024-002", "CLM-2024-003"],
        "customer_since": "2015-11-20",
        "tier": "Platinum",
    },
    "CUST-1004": {
        "customer_id": "CUST-1004",
        "name": "Sarah Martinez",
        "age": 42,
        "gender": "female",
        "marital_status": "married",
        "dependents": 3,
        "occupation": "small_business_owner",
        "annual_income": 220000,
        "state": "Texas",
        "city": "Austin",
        "credit_score": 750,
        "smoking_status": "non_smoker",
        "health_conditions": [],
        "driving_record": {"violations": 0, "accidents": 0, "years_licensed": 24},
        "active_policies": ["POL-BIZ-1004", "POL-AUTO-1004", "POL-HOME-1004"],
        "claims_history": ["CLM-2024-004"],
        "customer_since": "2018-01-10",
        "tier": "Gold",
    },
    "CUST-1005": {
        "customer_id": "CUST-1005",
        "name": "David Park",
        "age": 22,
        "gender": "male",
        "marital_status": "single",
        "dependents": 0,
        "occupation": "student",
        "annual_income": 25000,
        "state": "California",
        "city": "Los Angeles",
        "credit_score": 650,
        "smoking_status": "non_smoker",
        "health_conditions": [],
        "driving_record": {"violations": 2, "accidents": 1, "years_licensed": 4},
        "active_policies": [],
        "claims_history": ["CLM-2024-005"],
        "customer_since": "2024-01-05",
        "tier": "Standard",
    },
}


def lookup_customer(customer_id: str) -> dict:
    """Look up a customer profile by customer ID.

    Args:
        customer_id: The customer identifier (e.g., CUST-1001).

    Returns:
        Full customer profile with demographics, policies, and history.
    """
    customer = CUSTOMERS_DB.get(customer_id.upper())
    if customer:
        return {"found": True, "customer": customer}
    return {"found": False, "error": f"Customer not found: {customer_id}"}


def search_customer_by_name(name: str) -> dict:
    """Search for a customer by name (partial match).

    Args:
        name: Full or partial customer name.

    Returns:
        Matching customer profiles.
    """
    matches = []
    for cust in CUSTOMERS_DB.values():
        if name.lower() in cust["name"].lower():
            matches.append({
                "customer_id": cust["customer_id"],
                "name": cust["name"],
                "state": cust["state"],
                "tier": cust["tier"],
                "active_policies": len(cust["active_policies"]),
            })
    return {
        "query": name,
        "results_count": len(matches),
        "customers": matches,
    }
