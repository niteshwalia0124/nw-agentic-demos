"""Seed BigQuery with insurance compliance/regulatory data.

Creates state_regulations and federal_regulations tables and loads
the sample data from tools/compliance_checker.py.

Usage:
    python seed_bigquery.py
"""

from google.cloud import bigquery

import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
DATASET_ID = os.environ.get("BQ_DATASET", "insurance_compliance")

client = bigquery.Client(project=PROJECT_ID)



def create_and_load_state_regulations():
    table_id = f"{PROJECT_ID}.{DATASET_ID}.state_regulations"

    schema = [
        bigquery.SchemaField("state_code", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("state_name", "STRING"),
        bigquery.SchemaField("department", "STRING"),
        bigquery.SchemaField("auto_min_bodily_injury", "STRING"),
        bigquery.SchemaField("auto_min_property_damage", "INTEGER"),
        bigquery.SchemaField("rate_increase_cap_pct", "INTEGER"),
        bigquery.SchemaField("cancellation_notice_days", "INTEGER"),
        bigquery.SchemaField("claims_response_days", "INTEGER"),
        bigquery.SchemaField("discrimination_prohibited", "STRING", mode="REPEATED"),
        bigquery.SchemaField("required_coverages", "STRING", mode="REPEATED"),
        bigquery.SchemaField("required_discounts", "STRING", mode="REPEATED"),
        bigquery.SchemaField("data_privacy", "STRING"),
        bigquery.SchemaField("hurricane_moratorium", "BOOLEAN"),
        bigquery.SchemaField("sinkhole_coverage_required", "BOOLEAN"),
        bigquery.SchemaField("hail_damage_provisions", "BOOLEAN"),
    ]

    # Delete table if exists
    client.delete_table(table_id, not_found_ok=True)
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(f"  Created table {table_id}")

    rows = [
        {
            "state_code": "MH",
            "state_name": "Maharashtra",
            "department": "IRDAI Regional Office, Mumbai",
            "auto_min_bodily_injury": "Unlimited (Third Party)",
            "auto_min_property_damage": 750000,
            "rate_increase_cap_pct": 10,
            "cancellation_notice_days": 15,
            "claims_response_days": 30,
            "discrimination_prohibited": ["gender", "religion"],
            "required_coverages": ["third_party_liability"],
            "required_discounts": ["no_claim_bonus"],
            "data_privacy": "DPDP_Act",
            "hurricane_moratorium": False,
            "sinkhole_coverage_required": False,
            "hail_damage_provisions": False,
        },
        {
            "state_code": "KA",
            "state_name": "Karnataka",
            "department": "IRDAI Regional Office, Bangalore",
            "auto_min_bodily_injury": "Unlimited (Third Party)",
            "auto_min_property_damage": 750000,
            "rate_increase_cap_pct": 10,
            "cancellation_notice_days": 15,
            "claims_response_days": 30,
            "discrimination_prohibited": ["gender"],
            "required_coverages": ["third_party_liability"],
            "required_discounts": ["no_claim_bonus"],
            "data_privacy": "DPDP_Act",
            "hurricane_moratorium": False,
            "sinkhole_coverage_required": False,
            "hail_damage_provisions": False,
        },
        {
            "state_code": "DL",
            "state_name": "Delhi",
            "department": "IRDAI Head Office, Delhi",
            "auto_min_bodily_injury": "Unlimited (Third Party)",
            "auto_min_property_damage": 750000,
            "rate_increase_cap_pct": 10,
            "cancellation_notice_days": 15,
            "claims_response_days": 30,
            "discrimination_prohibited": [],
            "required_coverages": ["third_party_liability"],
            "required_discounts": ["no_claim_bonus"],
            "data_privacy": "DPDP_Act",
            "hurricane_moratorium": False,
            "sinkhole_coverage_required": False,
            "hail_damage_provisions": False,
        },
        {
            "state_code": "GJ",
            "state_name": "Gujarat",
            "department": "IRDAI Regional Office, Ahmedabad",
            "auto_min_bodily_injury": "Unlimited (Third Party)",
            "auto_min_property_damage": 750000,
            "rate_increase_cap_pct": 10,
            "cancellation_notice_days": 15,
            "claims_response_days": 30,
            "discrimination_prohibited": [],
            "required_coverages": ["third_party_liability"],
            "required_discounts": ["no_claim_bonus"],
            "data_privacy": "DPDP_Act",
            "hurricane_moratorium": False,
            "sinkhole_coverage_required": False,
            "hail_damage_provisions": False,
        },
    ]

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"  ERROR inserting state_regulations: {errors}")
    else:
        print(f"  Inserted {len(rows)} state regulations")


def create_and_load_federal_regulations():
    table_id = f"{PROJECT_ID}.{DATASET_ID}.federal_regulations"

    schema = [
        bigquery.SchemaField("regulation_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("requirements", "STRING", mode="REPEATED"),
        bigquery.SchemaField("applies_to", "STRING", mode="REPEATED"),
    ]

    client.delete_table(table_id, not_found_ok=True)
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(f"  Created table {table_id}")

    rows = [
        {
            "regulation_id": "irdai_protection",
            "name": "IRDAI (Protection of Policyholders' Interests) Regulations",
            "requirements": [
                "Claims must be settled within 30 days of all documents",
                "Clear disclosure of benefits and exclusions required",
                "Grievance redressal mechanism must be established",
            ],
            "applies_to": [],
        },
        {
            "regulation_id": "income_tax_80d",
            "name": "Income Tax Act - Section 80D",
            "requirements": [
                "Deduction up to ₹25,000 for self/family health premiums",
                "Additional ₹25,000/₹50,000 for parents",
                "Includes preventive health check-up deduction up to ₹5,000",
            ],
            "applies_to": ["health"],
        },
        {
            "regulation_id": "income_tax_80c",
            "name": "Income Tax Act - Section 80C",
            "requirements": [
                "Deduction up to ₹1.5 Lakh for life insurance premiums",
                "Policy must be active for at least 2 years for tax benefits",
            ],
            "applies_to": ["life"],
        },
        {
            "regulation_id": "motor_act",
            "name": "Motor Vehicles Act",
            "requirements": [
                "Third-party insurance is mandatory for all vehicles",
                "Penalty for driving without valid insurance",
            ],
            "applies_to": ["auto"],
        },
    ]

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"  ERROR inserting federal_regulations: {errors}")
    else:
        print(f"  Inserted {len(rows)} federal regulations")


def verify():
    print("\nVerification:")
    for table_name in ["state_regulations", "federal_regulations"]:
        query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}`"
        result = client.query(query).result()
        for row in result:
            print(f"  {table_name}: {row.cnt} rows")

    query = f"SELECT state_code, state_name, rate_increase_cap_pct FROM `{PROJECT_ID}.{DATASET_ID}.state_regulations` ORDER BY state_code"
    result = client.query(query).result()
    for row in result:
        print(f"  {row.state_code} | {row.state_name:>20} | cap: {row.rate_increase_cap_pct}%")


if __name__ == "__main__":
    print("Creating state_regulations table...")
    create_and_load_state_regulations()
    print("Creating federal_regulations table...")
    create_and_load_federal_regulations()
    verify()
    print("\nDone!")
