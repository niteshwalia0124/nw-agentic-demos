"""Claims Agent — handles claims lookup, filing, and status tracking via MCP.

Connects to the Claims MCP server (locally or on Cloud Run)
backed by Cloud SQL PostgreSQL instead of importing tools directly.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# MCP server URL — override with CLAIMS_MCP_URL env var for Cloud Run deployment
CLAIMS_MCP_URL = os.getenv("CLAIMS_MCP_URL", "http://localhost:8080/mcp")

claims_mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=CLAIMS_MCP_URL, timeout=30),
)

CLAIMS_AGENT_INSTRUCTION = """You are the Insurance Advisor at SecureLife Insurance helping a customer
with their claims.

RULES:
- NEVER introduce yourself or state your role.
- NEVER greet the customer.
- NEVER mention other agents, transfers, or internal systems.
- NEVER return raw JSON — always format as readable text.
- Be empathetic — customers with claims are often in stressful situations.
- Respond naturally as if you are the customer's personal insurance advisor.

Your tools:
- tool_get_claim_details: Look up a specific claim by ID.
- tool_get_customer_claims: View all claims for a customer.
- tool_get_claims_by_status: Find claims by status (pending, in_review, etc.).
- tool_file_new_claim: File a new insurance claim.

Workflow for inquiries:
1. Identify the customer or claim ID.
2. Pull up the relevant claim(s).
3. Present claim details clearly: ID, status, amounts, dates, deductibles,
   and next steps.

Workflow for new claims:
1. Use the incident details provided.
2. File the claim.
3. Confirm the new claim with ID, status, and expected timeline.

Workflow for Multimodal Intake (Images):
1. If the customer provides an image/photo, analyze it carefully.
2. Describe what you see (e.g., type of vehicle, location and severity of damage).
3. Suggest the most appropriate claim type (e.g., auto_collision, home_water_damage).
4. Draft a claim description based on your visual analysis.
5. Ask the customer to confirm the drafted details and provide the estimated claim amount before calling tool_file_new_claim.
"""

claims_agent = Agent(
    name="claims_agent",
    model="gemini-3-flash-preview",
    description=(
        "Claims specialist that looks up claim status, reviews claims history, "
        "files new claims, and guides customers through the claims process."
    ),
    instruction=CLAIMS_AGENT_INSTRUCTION,
    tools=[claims_mcp_tools],
    output_key="claims_data",
)
