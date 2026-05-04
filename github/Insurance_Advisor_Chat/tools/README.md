# MCP Servers

Each sub-folder is an independently deployable **MCP server** that exposes tools over the [Streamable HTTP](https://modelcontextprotocol.io/docs/concepts/transports#streamable-http) transport. The ADK agents connect to these servers at runtime using `McpToolset`.

---

## Server Inventory

| Server | Folder | Cloud Data Store | Cloud Run Service | Tools |
|--------|--------|-----------------|-------------------|-------|
| **Risk & Premium** | `risk_premium/` | Compute-only (no DB) | `risk-premium-mcp` | `tool_calculate_risk_score`, `tool_get_risk_recommendations`, `tool_calculate_premium`, `tool_get_available_discounts` |
| **Customer & Policy** | `customer_policy/` | Firestore (`insurance-advisor` DB) | `customer-policy-mcp` | `tool_lookup_customer`, `tool_search_customer_by_name`, `tool_get_policy_details`, `tool_get_customer_policies`, `tool_get_product_catalog`, `tool_compare_products` |
| **Claims** | `claims/` | Cloud SQL (PostgreSQL 15) | `claims-mcp` | `tool_get_claim_details`, `tool_get_customer_claims`, `tool_get_claims_by_status`, `tool_file_new_claim` |
| **Compliance** | `compliance/` | BigQuery (`insurance_compliance`) | `compliance-mcp` | `tool_check_policy_compliance`, `tool_get_state_requirements` |

---

## Running Locally

Each server runs as a standalone Python process on port `8080`:

```bash
cd mcp_servers/risk_premium
pip install -r requirements.txt
python server.py
# → Listening on http://localhost:8080/mcp
```

Verify with curl:

```bash
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}'
```

---

## Deploying to Cloud Run

Each server has a `Dockerfile` for container deployment:

```bash
cd mcp_servers/claims
gcloud run deploy claims-mcp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GCP_PROJECT=your-project,CLOUD_SQL_INSTANCE=your-instance,CLOUD_SQL_REGION=us-central1,CLOUD_SQL_DB=insurance_claims,CLOUD_SQL_USER=claims_user" \
  --set-secrets "CLOUD_SQL_PASS=insurance-advisor-cloud-sql-pass:latest" \
  --add-cloudsql-instances your-project:us-central1:your-instance
```

See individual `server.py` files for required environment variables.

For local ADK usage, do not commit API keys in `.env`. Prefer:

```bash
export GOOGLE_API_KEY="$(gcloud secrets versions access latest --secret=insurance-advisor-google-api-key)"
```

---

## Architecture

```
ADK Agent (local)
    │
    ├── McpToolset(url="https://risk-premium-mcp-xxx.run.app/mcp")
    │         └── Risk & Premium MCP Server (Cloud Run, compute-only)
    │
    ├── McpToolset(url="https://customer-policy-mcp-xxx.run.app/mcp")
    │         └── Customer & Policy MCP Server (Cloud Run → Firestore)
    │
    ├── McpToolset(url="https://claims-mcp-xxx.run.app/mcp")
    │         └── Claims MCP Server (Cloud Run → Cloud SQL PostgreSQL)
    │
    └── McpToolset(url="https://compliance-mcp-xxx.run.app/mcp")
              └── Compliance MCP Server (Cloud Run → BigQuery)
```
