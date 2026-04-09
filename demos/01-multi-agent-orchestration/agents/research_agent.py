"""Research agents — parallel trend and technical researchers.

Uses ADK's built-in ``google_search`` tool and ``ParallelAgent`` to run
two research specialists concurrently.  Each agent writes its findings
to shared state via ``output_key`` so downstream agents can reference
them through ADK state interpolation (``{trend_findings}`` /
``{technical_findings}``).
"""

from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.tools import google_search

from ..prompts.instructions import (
    TECHNICAL_RESEARCHER_INSTRUCTION,
    TREND_RESEARCHER_INSTRUCTION,
)

# --- State Keys ---
KEY_TREND_FINDINGS = "trend_findings"
KEY_TECHNICAL_FINDINGS = "technical_findings"

# --- Individual Research Agents ---

trend_researcher = LlmAgent(
    name="TrendResearcher",
    model="gemini-2.5-flash",
    instruction=TREND_RESEARCHER_INSTRUCTION,
    description=(
        "Searches for current trends, recent news, and emerging "
        "developments on the given topic."
    ),
    tools=[google_search],
    output_key=KEY_TREND_FINDINGS,
)

technical_researcher = LlmAgent(
    name="TechnicalResearcher",
    model="gemini-2.5-flash",
    instruction=TECHNICAL_RESEARCHER_INSTRUCTION,
    description=(
        "Searches for in-depth technical information, architectures, "
        "and best practices on the given topic."
    ),
    tools=[google_search],
    output_key=KEY_TECHNICAL_FINDINGS,
)

# --- Parallel Research Phase ---

parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[trend_researcher, technical_researcher],
    description="Runs trend and technical research in parallel.",
)
