"""Research Agent — searches the web and summarises findings."""

from google.adk.agents import Agent

from ..tools.web_search import web_search

RESEARCH_AGENT_INSTRUCTION = """You are a Research Agent specialising in finding and summarising information.

Your capabilities:
- Search the web for relevant information using the `web_search` tool.
- Analyse and synthesise information from multiple sources.
- Produce clear, well-structured summaries with key findings.

Guidelines:
1. When given a research task, break it into specific search queries.
2. Use the `web_search` tool to find relevant information.
3. Synthesise the results into a concise summary.
4. Always cite your sources when possible.
5. If search results are insufficient, state what you found and what gaps remain.
6. Focus on accuracy and relevance over volume.
"""

research_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description=(
        "Specialist agent for web research. Searches the internet, "
        "analyses sources, and produces concise summaries of findings."
    ),
    instruction=RESEARCH_AGENT_INSTRUCTION,
    tools=[web_search],
)
