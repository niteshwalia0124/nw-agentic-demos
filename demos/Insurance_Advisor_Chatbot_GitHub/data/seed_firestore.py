"""Seed the Firestore 'insurance-advisor' database with customer, policy, and product data."""

from google.cloud import firestore

PROJECT_ID = "butterfly-987"
DATABASE_ID = "insurance-advisor"

db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)

# ── Customers ───────────────────────────────────────────────────────────

CUSTOMERS = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "name": "Nitesh Walia",
        "age": 35,
        "gender": "male",
        "marital_status": "married",
        "dependents": 2,
        "occupation": "software_engineer",
        "annual_income": 2500000,
        "state": "Maharashtra",
        "city": "Mumbai",
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
        "name": "Ashish Kamble",
        "age": 28,
        "gender": "male",
        "marital_status": "single",
        "dependents": 0,
        "occupation": "marketing_manager",
        "annual_income": 1200000,
        "state": "Gujarat",
        "city": "Ahmedabad",
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
        "name": "Devesh Sati",
        "age": 62,
        "gender": "male",
        "marital_status": "married",
        "dependents": 0,
        "occupation": "retired",
        "annual_income": 900000,
        "state": "Delhi",
        "city": "New Delhi",
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
        "name": "Sourabh Jain",
        "age": 42,
        "gender": "male",
        "marital_status": "married",
        "dependents": 3,
        "occupation": "small_business_owner",
        "annual_income": 3500000,
        "state": "Karnataka",
        "city": "Bangalore",
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
        "name": "Ved Prakash",
        "age": 22,
        "gender": "male",
        "marital_status": "single",
        "dependents": 0,
        "occupation": "student",
        "annual_income": 300000,
        "state": "Telangana",
        "city": "Hyderabad",
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

# ── Products ────────────────────────────────────────────────────────────

PRODUCTS = {
    "AROGYA_SANJEEVANI": {
        "product_id": "AROGYA_SANJEEVANI",
        "name": "Arogya Sanjeevani Policy",
        "category": "health",
        "description": "Standard health insurance policy by IRDAI with uniform benefits",
        "coverage_options": {
            "sum_insured": [100000, 200000, 500000],
            "copay": 5,
            "room_rent_limit": "2% of sum insured",
        },
        "base_monthly_premium": 450.00,
        "features": ["AYUSH Coverage", "Pre/Post Hospitalization", "Tax Benefit 80D", "No claim bonus"],
        "eligibility": {"min_age": 0, "max_age": 65},
    },
    "SECURE_HEALTH_PREMIUM": {
        "product_id": "SECURE_HEALTH_PREMIUM",
        "name": "Demo Insurance Health Premium",
        "category": "health",
        "description": "Premium health plan with enhanced coverage, zero copay, and critical illness coverage",
        "coverage_options": {
            "sum_insured": [1000000, 1500000, 2500000],
            "copay": 0,
        },
        "base_monthly_premium": 850.00,
        "features": ["Maternity Benefit", "Critical Illness", "OPD Cover", "No claim bonus"],
        "eligibility": {"min_age": 0, "max_age": 75},
    },
    "SECURE_HEALTH_STANDARD": {
        "product_id": "SECURE_HEALTH_STANDARD",
        "name": "Demo Insurance Health Standard",
        "category": "health",
        "description": "Affordable and standard individual health insurance plan",
        "coverage_options": {
            "sum_insured": [300000, 500000],
            "copay": 10,
        },
        "base_monthly_premium": 350.00,
        "features": ["In-patient Care", "Ambulance Cover", "Tax Benefit 80D"],
        "eligibility": {"min_age": 0, "max_age": 65},
    },
    "JEEVAN_ANAND": {
        "product_id": "JEEVAN_ANAND",
        "name": "Demo Insurance Jeevan Anand",
        "category": "life",
        "description": "Endowment plan with bonus and survival benefits",
        "coverage_range": {"min": 100000, "max": 5000000},
        "term_options_years": [15, 20, 30],
        "base_monthly_premium": 2500.00,
        "features": ["Bonus Facility", "Survival Benefit", "Tax Benefit 80C", "Loan against policy"],
        "eligibility": {"min_age": 18, "max_age": 50},
    },
    "SARAL_JEEVAN_BIMA": {
        "product_id": "SARAL_JEEVAN_BIMA",
        "name": "Demo Insurance Saral Jeevan Bima",
        "category": "life",
        "description": "Simple pure term life insurance offering complete financial security",
        "coverage_range": {"min": 500000, "max": 2500000},
        "term_options_years": [10, 20, 30],
        "base_monthly_premium": 1200.00,
        "features": ["Pure Term Cover", "High Sum Assured", "Tax Benefit 80C"],
        "eligibility": {"min_age": 18, "max_age": 65},
    },
    "SMART_ELITE_SAVINGS": {
        "product_id": "SMART_ELITE_SAVINGS",
        "name": "Demo Insurance Smart Elite Savings",
        "category": "life",
        "description": "Premium market linked investment and savings protection plan",
        "coverage_range": {"min": 1000000, "max": 10000000},
        "term_options_years": [5, 10, 15],
        "base_monthly_premium": 3500.00,
        "features": ["Market Linked Growth", "Death Benefit", "Flexible Premium", "Wealth Additions"],
        "eligibility": {"min_age": 18, "max_age": 60},
    },
    "AUTO_COMPREHENSIVE": {
        "product_id": "AUTO_COMPREHENSIVE",
        "name": "DriveShield Comprehensive",
        "category": "auto",
        "description": "Covers Own Damage and Third Party Liability with Indian add-ons",
        "coverage_options": {
            "third_party_limit": "Mandatory IRDAI rates",
            "own_damage_deductible": [1000, 2500],
            "add_ons": ["Zero Depreciation", "Return to Invoice", "Engine Protector"],
        },
        "base_monthly_premium": 850.00,
        "features": ["Zero Depreciation", "24x7 Roadside Assistance", "Personal Accident Cover"],
        "eligibility": {"min_age": 18, "max_age": 99},
    },
    "AUTO_PREMIUM": {
        "product_id": "AUTO_PREMIUM",
        "name": "DriveShield Premium Plus",
        "category": "auto",
        "description": "Premium auto cover with all top tier add-ons and low deductible",
        "coverage_options": {
            "third_party_limit": "Mandatory IRDAI rates",
            "own_damage_deductible": [500],
            "add_ons": ["Zero Depreciation", "Return to Invoice", "Engine Protector", "Roadside Assistance"],
        },
        "base_monthly_premium": 1150.00,
        "features": ["Zero Depreciation", "Return to Invoice", "Engine Protector", "Roadside Assistance"],
        "eligibility": {"min_age": 18, "max_age": 99},
    },
    "AUTO_STANDARD": {
        "product_id": "AUTO_STANDARD",
        "name": "DriveShield Lite",
        "category": "auto",
        "description": "Standard cost effective car insurance plan",
        "coverage_options": {
            "third_party_limit": "Mandatory IRDAI rates",
            "own_damage_deductible": [3000],
        },
        "base_monthly_premium": 450.00,
        "features": ["Third Party Liability", "Towing Cover", "Basic Damage Protection"],
        "eligibility": {"min_age": 18, "max_age": 99},
    },
    "BHARAT_GRIHA_RAKSHA": {
        "product_id": "BHARAT_GRIHA_RAKSHA",
        "name": "Bharat Griha Raksha",
        "category": "home",
        "description": "Standard home insurance policy covering structure and contents",
        "coverage_options": {
            "dwelling": {"min": 500000, "max": 50000000},
            "contents": "Automatic 20% of dwelling",
            "deductible": [0],
        },
        "base_monthly_premium": 200.00,
        "features": ["No under-insurance", "Rent for alternative accommodation", "Debris removal"],
        "eligibility": {"property_types": ["apartment", "bungalow"]},
    },
    "HOME_SECURE_DELUXE": {
        "product_id": "HOME_SECURE_DELUXE",
        "name": "SecureHome Deluxe Plan",
        "category": "home",
        "description": "Premium and all inclusive home insurance plan",
        "coverage_options": {
            "dwelling": {"min": 1000000, "max": 100000000},
            "contents": "Up to 40% of dwelling",
        },
        "base_monthly_premium": 550.00,
        "features": ["Earthquake/Flood Cover", "Burglary Cover", "Jewelry & Valuables Add-on"],
        "eligibility": {"property_types": ["apartment", "bungalow", "villa"]},
    },
    "HOME_SECURE_ESSENTIAL": {
        "product_id": "HOME_SECURE_ESSENTIAL",
        "name": "SecureHome Essential Plan",
        "category": "home",
        "description": "Essential low cost home structure insurance plan",
        "coverage_options": {
            "dwelling": {"min": 300000, "max": 20000000},
        },
        "base_monthly_premium": 150.00,
        "features": ["Fire & Storm Protection", "Tenant Liability Cover"],
        "eligibility": {"property_types": ["apartment", "bungalow", "rented_home"]},
    },
}

# ── Active Policies ─────────────────────────────────────────────────────

POLICIES = {
    "POL-AUTO-1001": {
        "policy_id": "POL-AUTO-1001",
        "customer_id": "CUST-1001",
        "product_id": "AUTO_COMPREHENSIVE",
        "product_name": "DriveShield Comprehensive",
        "status": "active",
        "effective_date": "2024-01-15",
        "expiration_date": "2025-01-15",
        "monthly_premium": 1200.00,
        "coverage_summary": {"liability": "Third Party", "own_damage_deductible": 1000, "add_ons": ["Zero Dep"]},
        "vehicle": {"year": 2022, "make": "Maruti", "model": "Brezza", "vin": "MH01CJ1234"},
    },
    "POL-HOME-1001": {
        "policy_id": "POL-HOME-1001",
        "customer_id": "CUST-1001",
        "product_id": "BHARAT_GRIHA_RAKSHA",
        "product_name": "Bharat Griha Raksha",
        "status": "active",
        "effective_date": "2023-06-01",
        "expiration_date": "2024-06-01",
        "monthly_premium": 250.00,
        "coverage_summary": {"dwelling": 15000000, "contents": 3000000},
    },
    "POL-AUTO-1002": {
        "policy_id": "POL-AUTO-1002",
        "customer_id": "CUST-1002",
        "product_id": "AUTO_COMPREHENSIVE",
        "product_name": "DriveShield Comprehensive",
        "status": "active",
        "effective_date": "2024-03-01",
        "expiration_date": "2025-03-01",
        "monthly_premium": 950.00,
        "coverage_summary": {"liability": "Third Party", "own_damage_deductible": 2500},
        "vehicle": {"year": 2023, "make": "Hyundai", "model": "i20", "vin": "GJ01AP5678"},
    },
    "POL-HOME-1003": {
        "policy_id": "POL-HOME-1003",
        "customer_id": "CUST-1003",
        "product_id": "BHARAT_GRIHA_RAKSHA",
        "product_name": "Bharat Griha Raksha",
        "status": "active",
        "effective_date": "2023-01-01",
        "expiration_date": "2024-01-01",
        "monthly_premium": 180.00,
        "coverage_summary": {"dwelling": 8000000, "contents": 1600000},
    },
    "POL-LIFE-1003": {
        "policy_id": "POL-LIFE-1003",
        "customer_id": "CUST-1003",
        "product_id": "JEEVAN_ANAND",
        "product_name": "Demo Insurance Jeevan Anand",
        "status": "active",
        "effective_date": "2015-11-20",
        "expiration_date": "2035-11-20",
        "monthly_premium": 3500.00,
        "coverage_summary": {"sum_assured": 1000000, "accidental_death_benefit": 1000000},
    },
    "POL-HEALTH-1003": {
        "policy_id": "POL-HEALTH-1003",
        "customer_id": "CUST-1003",
        "product_id": "AROGYA_SANJEEVANI",
        "product_name": "Arogya Sanjeevani Policy",
        "status": "active",
        "effective_date": "2024-01-01",
        "expiration_date": "2024-12-31",
        "monthly_premium": 650.00,
        "coverage_summary": {"sum_insured": 500000, "copay": 5},
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
        "business": {"name": "Iyer Catering Services", "type": "food_service", "employees": 8},
    },
    "POL-AUTO-1004": {
        "policy_id": "POL-AUTO-1004",
        "customer_id": "CUST-1004",
        "product_id": "AUTO_COMPREHENSIVE",
        "product_name": "DriveShield Comprehensive",
        "status": "active",
        "effective_date": "2024-05-01",
        "expiration_date": "2025-05-01",
        "monthly_premium": 1700.00,
        "coverage_summary": {"liability": "Third Party", "own_damage_deductible": 1000},
    },
    "POL-HOME-1004": {
        "policy_id": "POL-HOME-1004",
        "customer_id": "CUST-1004",
        "product_id": "BHARAT_GRIHA_RAKSHA",
        "product_name": "Bharat Griha Raksha",
        "status": "active",
        "effective_date": "2024-01-15",
        "expiration_date": "2025-01-15",
        "monthly_premium": 1500.00,
        "coverage_summary": {"dwelling": 25000000, "contents": 5000000},
    },
}


def seed():
    print("Seeding Firestore database: insurance-advisor")

    # Seed customers
    for cust_id, data in CUSTOMERS.items():
        db.collection("customers").document(cust_id).set(data)
        print(f"  + customers/{cust_id}")

    # Seed products
    for prod_id, data in PRODUCTS.items():
        db.collection("products").document(prod_id).set(data)
        print(f"  + products/{prod_id}")

    # Seed policies
    for pol_id, data in POLICIES.items():
        db.collection("policies").document(pol_id).set(data)
        print(f"  + policies/{pol_id}")

    print(f"\nDone: {len(CUSTOMERS)} customers, {len(PRODUCTS)} products, {len(POLICIES)} policies")


if __name__ == "__main__":
    seed()
