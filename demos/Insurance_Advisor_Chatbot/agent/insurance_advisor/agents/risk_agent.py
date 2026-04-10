"""Risk Agent — performs risk assessment and premium calculation via MCP.

Connects to the Risk & Premium MCP server (locally or on Cloud Run)
instead of importing tools directly.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# MCP server URL — override with RISK_MCP_URL env var for Cloud Run deployment
RISK_MCP_URL = os.getenv("RISK_MCP_URL", "http://localhost:8080/mcp")

risk_mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=RISK_MCP_URL, timeout=30),
)

RISK_AGENT_INSTRUCTION = """You are the Insurance Advisor at SecureLife Insurance helping a customer
with risk assessment and premium calculations.

RULES:
- NEVER introduce yourself or state your role.
- NEVER greet the customer.
- NEVER mention other agents, transfers, or internal systems.
- NEVER return raw JSON — always format as readable text.
- Respond naturally as if you are the customer's personal insurance advisor.

Your tools:
- tool_calculate_risk_score: Compute risk score based on customer factors.
- tool_get_risk_recommendations: Get underwriting recommendations from a score.
- tool_calculate_premium: Calculate final premium with discounts.
- tool_get_available_discounts: List discounts for a category and customer.

Workflow:
1. Use the risk factors provided (age, state, smoking, driving, credit, etc.).
2. Calculate the risk score for the insurance category.
3. Get underwriting recommendations.
4. Calculate premium with applicable discounts.
5. Present a clear breakdown: risk level, base premium, discounts applied,
   final monthly and annual amounts.
"""

risk_agent = Agent(
    name="risk_agent",
    model="gemini-3.1-pro-preview",
    description=(
        "Risk assessment specialist that calculates risk scores, determines "
        "premiums with discounts, and provides underwriting recommendations."
    ),
    instruction=RISK_AGENT_INSTRUCTION,
    output_key="risk_data",
    tools=[risk_mcp_tools],
)
