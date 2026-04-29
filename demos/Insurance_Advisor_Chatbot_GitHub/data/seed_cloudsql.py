"""Seed Cloud SQL PostgreSQL with insurance claims data.

Creates the claims table and inserts sample records matching
the data from tools/claims_db.py.

Usage:
    python seed_cloudsql.py
"""

import sqlalchemy
from google.cloud.sql.connector import Connector


import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
REGION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
INSTANCE_NAME = os.environ.get("CLOUD_SQL_INSTANCE", "YOUR_INSTANCE_NAME")
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
DB_NAME = os.environ.get("CLOUD_SQL_DB", "insurance_claims")
DB_USER = os.environ.get("CLOUD_SQL_USER", "claims_user")
DB_PASS = os.environ.get("CLOUD_SQL_PASS", "YOUR_DB_PASSWORD")


def get_engine():
    connector = Connector()

    def getconn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine


def create_tables(engine):
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
            DROP TABLE IF EXISTS claims CASCADE;
            CREATE TABLE claims (
                claim_id        VARCHAR(20) PRIMARY KEY,
                policy_id       VARCHAR(20) NOT NULL,
                customer_id     VARCHAR(20) NOT NULL,
                claim_type      VARCHAR(50) NOT NULL,
                status          VARCHAR(30) NOT NULL,
                filed_date      DATE NOT NULL,
                resolved_date   DATE,
                description     TEXT NOT NULL,
                amount_claimed  DECIMAL(12,2) NOT NULL,
                amount_approved DECIMAL(12,2),
                deductible_applied DECIMAL(12,2),
                fault           VARCHAR(30),
                adjuster        VARCHAR(100),
                documents       TEXT[]
            );

            CREATE INDEX idx_claims_customer ON claims(customer_id);
            CREATE INDEX idx_claims_status ON claims(status);
            CREATE INDEX idx_claims_policy ON claims(policy_id);
        """))
    print("Tables created.")


def seed_data(engine):
    claims = [
        {
            "claim_id": "CLM-2024-001",
            "policy_id": "POL-AUTO-1001",
            "customer_id": "CUST-1001",
            "claim_type": "auto_collision",
            "status": "closed",
            "filed_date": "2024-04-12",
            "resolved_date": "2024-05-20",
            "description": "Rear-ended near Western Express Highway, Goregaon. Damage to rear bumper and tailgate.",
            "amount_claimed": 45000.00,
            "amount_approved": 38000.00,
            "deductible_applied": 2000.00,
            "fault": "other_party",
            "adjuster": "Sandeep Mehta",
            "documents": ["police_report.pdf", "damage_photos.zip", "repair_estimate.pdf"],
        },
        {
            "claim_id": "CLM-2024-002",
            "policy_id": "POL-HOME-1003",
            "customer_id": "CUST-1003",
            "claim_type": "home_water_damage",
            "status": "in_review",
            "filed_date": "2024-09-03",
            "resolved_date": None,
            "description": "Seepage damage to living room ceiling due to heavy Mumbai monsoons and terrace leakage.",
            "amount_claimed": 85000.00,
            "amount_approved": None,
            "deductible_applied": 5000.00,
            "fault": "not_applicable",
            "adjuster": "Priyanka Das",
            "documents": ["damage_photos.zip", "surveyor_report.pdf"],
        },
        {
            "claim_id": "CLM-2024-003",
            "policy_id": "POL-AUTO-1004",
            "customer_id": "CUST-1004",
            "claim_type": "auto_comprehensive",
            "status": "approved",
            "filed_date": "2024-07-15",
            "resolved_date": "2024-08-01",
            "description": "Windshield cracked due to a stone flying off a truck on the Bangalore-Mysore Expressway.",
            "amount_claimed": 12000.00,
            "amount_approved": 11500.00,
            "deductible_applied": 1000.00,
            "fault": "unavoidable_accident",
            "adjuster": "Karthik Raja",
            "documents": ["incident_photos.zip", "repair_invoice.pdf"],
        },
        {
            "claim_id": "CLM-2024-004",
            "policy_id": "POL-HEALTH-1003",
            "customer_id": "CUST-1003",
            "claim_type": "health_hospitalization",
            "status": "closed",
            "filed_date": "2024-06-20",
            "resolved_date": "2024-07-15",
            "description": "Hospitalization for Dengue fever treatment at Max Super Speciality Hospital.",
            "amount_claimed": 125000.00,
            "amount_approved": 110000.00,
            "deductible_applied": 5000.00,
            "fault": "not_applicable",
            "adjuster": "Auto-processed",
            "documents": ["discharge_summary.pdf", "medical_bills.pdf"],
        },
    ]

    with engine.begin() as conn:
        for claim in claims:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO claims (claim_id, policy_id, customer_id, claim_type, status,
                        filed_date, resolved_date, description, amount_claimed, amount_approved,
                        deductible_applied, fault, adjuster, documents)
                    VALUES (:claim_id, :policy_id, :customer_id, :claim_type, :status,
                        :filed_date, :resolved_date, :description, :amount_claimed, :amount_approved,
                        :deductible_applied, :fault, :adjuster, :documents)
                    ON CONFLICT (claim_id) DO NOTHING
                """),
                {
                    **claim,
                    "documents": claim["documents"],
                },
            )
            print(f"  Inserted {claim['claim_id']}")

    print(f"Seeded {len(claims)} claims.")


def verify(engine):
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM claims"))
        count = result.scalar()
        print(f"\nVerification: {count} claims in database.")

        result = conn.execute(sqlalchemy.text(
            "SELECT claim_id, customer_id, status, amount_claimed FROM claims ORDER BY claim_id"
        ))
        for row in result:
            print(f"  {row[0]} | {row[1]} | {row[2]:>20} | ${row[3]:,.2f}")


if __name__ == "__main__":
    print("Connecting to Cloud SQL...")
    engine = get_engine()
    print("Creating tables...")
    create_tables(engine)
    print("Seeding data...")
    seed_data(engine)
    verify(engine)
    print("\nDone!")
