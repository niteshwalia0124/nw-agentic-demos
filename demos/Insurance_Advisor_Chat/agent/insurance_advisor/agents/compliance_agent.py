"""Compliance Agent — validates regulatory compliance via MCP.

Connects to the Compliance MCP server (locally or on Cloud Run)
backed by BigQuery instead of importing tools directly.
"""

import os

from google.adk.agents import Agent
from google.adk.integrations.agent_registry import AgentRegistry
from google.auth import default

_, project_id = default()
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
registry = AgentRegistry(project_id=project_id, location=LOCATION)

compliance_mcp_tools = registry.get_mcp_toolset(
    f"projects/{project_id}/locations/{LOCATION}/mcpServers/YOUR_COMPLIANCE_MCP_SERVER_ID"
)


COMPLIANCE_AGENT_INSTRUCTION = """\
You are the Insurance Advisor at Insurance AI Assistant helping a customer
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
3. Proactively present all compliance items, warnings, and violations together in a single Unified Compliance Dashboard (Markdown table) upfront for a high-quality visual overview.
4. If a warning or violation exists, proactively suggest the immediate corrective action to resolve it. If it is fully compliant, state clearly that it passed all checks.

If a tool call fails due to a technical or connection error, respond gracefully with:
"I'm having a little trouble accessing compliance records right now. Could you try again in a moment?"
"""

compliance_agent = Agent(
    name="compliance_agent",
    model="gemini-3.1-flash-lite-preview",
    description=(
        "Compliance specialist that validates insurance policies and operations "
        "against state and national regulations, flags violations, and provides guidance."
    ),
    instruction=COMPLIANCE_AGENT_INSTRUCTION,
    tools=[compliance_mcp_tools],
    output_key="compliance_data",
)
