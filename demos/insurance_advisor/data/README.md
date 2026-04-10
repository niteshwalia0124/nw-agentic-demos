# Data Seeding Scripts

One-time scripts to populate cloud data stores with sample insurance data.

Run these **before** testing the MCP servers or ADK agents.

---

## Scripts

| Script | Target Store | What It Seeds |
|--------|-------------|---------------|
| `seed_firestore.py` | Firestore (`insurance-advisor` DB) | 5 customers, 6 products, 8 policies |
| `seed_cloudsql.py` | Cloud SQL PostgreSQL (`insurance_claims` DB) | 6 sample claims |
| `seed_bigquery.py` | BigQuery (`insurance_compliance` dataset) | 4 state regulations + 4 federal regulations |

---

## Usage

```bash
# Ensure GCP credentials are configured
gcloud auth application-default login

# From the insurance_advisor/ directory
cd data

# Seed Firestore (customers, products, policies)
python seed_firestore.py

# Seed Cloud SQL (claims)
python seed_cloudsql.py

# Seed BigQuery (compliance regulations)
python seed_bigquery.py
```

> **Note:** The Risk & Premium MCP server is compute-only and requires no seeding.
