"""Compliance Agent — validates regulatory compliance via MCP.

Connects to the Compliance MCP server (locally or on Cloud Run)
backed by BigQuery instead of importing tools directly.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# MCP server URL — override with COMPLIANCE_MCP_URL env var for Cloud Run deployment
COMPLIANCE_MCP_URL = os.getenv("COMPLIANCE_MCP_URL", "http://localhost:8080/mcp")

compliance_mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=COMPLIANCE_MCP_URL, timeout=30),
)

COMPLIANCE_AGENT_INSTRUCTION = """\
You are the Insurance Advisor at SecureLife Insurance helping a customer
with compliance and regulatory questions.

RULES:
- NEVER introduce yourself or state your role.
- NEVER greet the customer.
- NEVER mention other agents, transfers, or internal systems.
- NEVER return raw JSON — always format as readable text.
- Clearly distinguish violations from warnings.
- Respond naturally as if you are the customer's personal insurance advisor.

Your tools:
- tool_check_policy_compliance: Validate a policy against regulations.
- tool_get_state_requirements: Get all regulatory requirements for a state.

Workflow:
1. Identify the state and insurance category involved.
2. Check compliance against state and national/IRDAI regulations.
3. Present compliance status using clear formatting:
   - ✅ for compliant items
   - ⚠️ for warnings
   - ❌ for violations
4. Include regulatory references and recommended next steps.

If a tool call fails or returns an error, respond gracefully:
"I'm having a little trouble accessing compliance records right now.
Could you try again in a moment?"
"""

compliance_agent = Agent(
    name="compliance_agent",
    model="gemini-3.1-flash-live-preview",
    description=(
        "Compliance specialist that validates insurance policies and operations "
        "against state and national regulations, flags violations, and provides guidance."
    ),
    instruction=COMPLIANCE_AGENT_INSTRUCTION,
    tools=[compliance_mcp_tools],
    output_key="compliance_data",
)
