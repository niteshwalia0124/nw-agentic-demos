# Insurance Advisor - Multi-Agent + MCP on Google Cloud

Prototype insurance advisory platform built with Google ADK. It provides one unified conversational advisor backed by four specialist agents and four custom MCP servers running on Cloud Run.

## What This Advisor Is

Insurance Advisor is a hierarchical multi-agent system where a root advisor orchestrates specialist agents for policy, risk, claims, and compliance tasks.

Current root persona:
- Name: Bima Sahayak
- Style: Indian-context conversational advisor (Hinglish-friendly)
- Goal: Deliver practical insurance guidance focused on Suraksha (protection) and Bachat (value/tax efficiency)

Core architecture:
- Root ADK agent delegates to specialist sub-agents
- Each specialist uses MCP tools over Streamable HTTP
- Each MCP server is deployed independently to Cloud Run
- Data is served from Google Cloud managed services

## What Has Been Done So Far

The platform has been actively updated and verified end-to-end.

Completed updates:
- Indianized advisor behavior and customer context in orchestrator prompts
- Model upgraded to Gemini 3.1 Pro preview for orchestrator and specialists
- Session state initialization and events compaction added for stronger multi-turn behavior
- Firestore seed data updated with Indianized customers, products, and policies
- Cloud SQL seed data updated with localized claims examples
- BigQuery seed data updated with Indian regional/state regulatory mappings
- All 4 custom MCP servers were deleted and redeployed fresh on Cloud Run
- MCP endpoints were smoke-tested with initialize calls after redeploy
- ADK orchestration was smoke-tested against live MCP backends
- Claims MCP password handling hardened:
- Removed hardcoded DB password fallback in claims MCP
- Enforced runtime secret injection for claims DB password
- Connected claims deployment to Secret Manager
- Local env cleaned to avoid storing live keys in source

## How This Advisor Helps Users

The advisor can assist users with practical insurance journeys in one conversation:

1. Policy and account help
- Find customer profile by ID or name
- Show active policies and coverage summary
- Explain policy details and compare products

2. Risk and premium guidance
- Estimate risk score using profile factors
- Provide underwriting recommendations
- Calculate premium and applicable discounts

3. Claims support
- Fetch claim history and claim details
- Track claim status
- File a new claim with next steps

4. Compliance and regulatory guidance
- Validate policy changes against regional rules
- Flag violations and warnings
- Explain relevant regulatory references

5. Combined advisory flows
- Coverage gap + compliance checks
- Premium optimization + discount recommendations
- Claims + policy context in one unified response

## System Components

ADK agent layer:
- root advisor: [agent.py](agent.py)
- specialists: [agents/policy_agent.py](agents/policy_agent.py), [agents/risk_agent.py](agents/risk_agent.py), [agents/claims_agent.py](agents/claims_agent.py), [agents/compliance_agent.py](agents/compliance_agent.py)

MCP servers:
- risk and premium: [mcp_servers/risk_premium/server.py](mcp_servers/risk_premium/server.py)
- customer and policy (Firestore): [mcp_servers/customer_policy/server.py](mcp_servers/customer_policy/server.py)
- claims (Cloud SQL): [mcp_servers/claims/server.py](mcp_servers/claims/server.py)
- compliance (BigQuery): [mcp_servers/compliance/server.py](mcp_servers/compliance/server.py)

Seed scripts:
- [data/seed_firestore.py](data/seed_firestore.py)
- [data/seed_cloudsql.py](data/seed_cloudsql.py)
- [data/seed_bigquery.py](data/seed_bigquery.py)

## Current Cloud Run MCP Services

- risk-premium-mcp
- customer-policy-mcp
- claims-mcp
- compliance-mcp

Environment wiring for these endpoints is configured in [.env](.env).

## Quick Start

1. Install dependencies

pip install -r requirements.txt

2. Configure environment

cp .env.example .env

3. Set API key securely (recommended)

export GOOGLE_API_KEY="$(gcloud secrets versions access latest --secret=insurance-advisor-google-api-key --project butterfly-987)"

4. Seed data stores

cd data
python seed_firestore.py
python seed_cloudsql.py
python seed_bigquery.py

5. Run the advisor

From the demos parent directory:

adk web .

Then select insurance_advisor in the ADK Web UI.

## Security Notes

- Do not commit live keys in .env.
- Use Secret Manager for Cloud SQL password and API keys.
- Claims MCP now requires CLOUD_SQL_PASS at runtime and should be deployed with set-secrets.

## Sample User Prompts

- Rajesh-ji ke current policies aur monthly premium breakdown dikhaiye.
- 35-year-old driver in MH ke liye auto premium estimate kijiye with safe driver discount.
- CUST-1003 ka claims history bataiye and pending claim next steps samjhaiye.
- MH home policy me 12 percent rate increase compliant hai kya?
- Mere current cover ke basis pe bataiye where I am underinsured and what to improve first.

## Prototype Scope

This is a prototype intended for rapid experimentation and demos. It is suitable for:
- Multi-agent orchestration demonstrations
- MCP server separation patterns
- Cloud Run based agent-tool backends
- Insurance workflow prototyping

For production hardening, add stricter auth, audit logging, guardrails, and formal eval suites.
