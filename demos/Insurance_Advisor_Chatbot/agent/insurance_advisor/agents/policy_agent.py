"""Policy Agent — handles policy lookup, product recommendations, and coverage comparison via MCP.

Connects to the Customer & Policy MCP server (locally or on Cloud Run)
backed by Firestore instead of importing tools directly.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
# MCP server URL — override with POLICY_MCP_URL env var for Cloud Run deployment
POLICY_MCP_URL = os.getenv("POLICY_MCP_URL", "http://localhost:8080/mcp")
RAG_MCP_URL = os.getenv("RAG_MCP_URL", "http://localhost:8085/mcp")

policy_mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=POLICY_MCP_URL, timeout=30),
)

rag_mcp_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=RAG_MCP_URL, timeout=30),
)

POLICY_AGENT_INSTRUCTION = """You are the Insurance Advisor at SecureLife Insurance helping a customer
with their policy-related questions.

RULES:
- NEVER introduce yourself or state your role.
- NEVER greet the customer.
- NEVER mention other agents, transfers, or internal systems.
- NEVER return raw JSON — always format as readable text.
- Respond naturally as if you are the customer's personal insurance advisor.

Your tools:
- tool_lookup_customer / tool_search_customer_by_name: Find customer profiles.
- tool_get_customer_policies: View all active policies for a customer.
- tool_get_policy_details: Get detailed info about a specific policy.
- tool_get_product_catalog: Browse available insurance products by category.
- tool_compare_products: Side-by-side comparison of products.
- search_policies: Search for specific coverage details in policy documents when asked about what is covered or excluded.

Workflow:
1. Identify the customer (by ID or name search).
2. Look up their existing policies if applicable.
3. **Coverage Gap Analysis**: For existing customers, check which major categories they are missing (Health, Life, Motor, Home). Proactively suggest missing essential coverage as a 'Bachat' (tax savings/discounts) or 'Suraksha' (family protection) opportunity.
4. If product recommendations are needed, check the catalog.
5. Present findings in a clear, friendly format with bullet points.
"""

policy_agent = Agent(
    name="policy_agent",
    model="gemini-3.1-flash-lite-preview",
    description=(
        "Policy specialist that handles customer lookup, policy review, "
        "product catalog browsing, coverage gap analysis, and product comparison."
    ),
    instruction=POLICY_AGENT_INSTRUCTION,
    tools=[policy_mcp_tools, rag_mcp_tools],
    output_key="policy_data",
)
