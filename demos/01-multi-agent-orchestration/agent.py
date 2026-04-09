"""Multi-Agent Orchestration Demo — Content Creation Pipeline.

A ``SequentialAgent`` pipeline that showcases all four ADK orchestration
primitives — ``SequentialAgent``, ``ParallelAgent``, ``LoopAgent``, and
``LlmAgent`` — to turn a user-supplied topic into a polished article.

Pipeline stages:
  1. **Topic Analyzer** (LlmAgent) — produces a research plan.
  2. **Parallel Research** (ParallelAgent) — trend + technical research.
  3. **Parallel Content** (ParallelAgent) — creative writer, technical
     writer, and code-example writer running concurrently.
  4. **Content Synthesizer** (LlmAgent) — merges all drafts.
  5. **Review Loop** (LoopAgent ▸ SequentialAgent) — iterative
     critique-then-revise cycle.
  6. **Final Editor** (LlmAgent) — polishes the final output.

Usage:
    adk run agent.py
"""

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

from .agents.code_agent import code_agent
from .agents.research_agent import parallel_research
from .agents.reviewer_agent import review_loop
from .agents.writer_agent import parallel_writers
from .prompts.instructions import (
    CONTENT_SYNTHESIZER_INSTRUCTION,
    FINAL_EDITOR_INSTRUCTION,
    TOPIC_ANALYZER_INSTRUCTION,
)

# --- State Keys ---
KEY_RESEARCH_PLAN = "research_plan"
KEY_MERGED_DRAFT = "merged_draft"
KEY_FINAL_CONTENT = "final_content"


# --- Before-model callback: initialise shared state ---
def _init_pipeline_state(callback_context, llm_request):
    """Set default values for state keys so downstream prompts render cleanly."""
    defaults = {
        KEY_RESEARCH_PLAN: "",
        "trend_findings": "",
        "technical_findings": "",
        "creative_draft": "",
        "technical_draft": "",
        "code_examples": "",
        KEY_MERGED_DRAFT: "",
        "review_feedback": "",
        KEY_FINAL_CONTENT: "",
    }
    for key, value in defaults.items():
        callback_context.state.setdefault(key, value)


# ---------------------------------------------------------------------------
# Stage 1 — Topic Analysis
# ---------------------------------------------------------------------------
topic_analyzer = LlmAgent(
    name="TopicAnalyzer",
    model="gemini-2.5-flash",
    instruction=TOPIC_ANALYZER_INSTRUCTION,
    description="Analyses the user's topic and creates a structured research plan.",
    output_key=KEY_RESEARCH_PLAN,
    before_model_callback=_init_pipeline_state,
)

# ---------------------------------------------------------------------------
# Stage 2 — Parallel Research  (imported from agents/)
# ---------------------------------------------------------------------------
# parallel_research is a ParallelAgent with TrendResearcher + TechnicalResearcher

# ---------------------------------------------------------------------------
# Stage 3 — Parallel Content Creation
# ---------------------------------------------------------------------------
# parallel_writers (creative + technical) imported from agents/
# code_agent imported separately so we can run all three concurrently.
parallel_content = ParallelAgent(
    name="ParallelContent",
    sub_agents=[parallel_writers, code_agent],
    description=(
        "Runs creative writer, technical writer, and code-example "
        "writer concurrently."
    ),
)

# ---------------------------------------------------------------------------
# Stage 4 — Content Synthesis
# ---------------------------------------------------------------------------
content_synthesizer = LlmAgent(
    name="ContentSynthesizer",
    model="gemini-2.5-flash",
    instruction=CONTENT_SYNTHESIZER_INSTRUCTION,
    description=(
        "Merges the creative draft, technical draft, and code examples "
        "into a single cohesive article."
    ),
    output_key=KEY_MERGED_DRAFT,
)

# ---------------------------------------------------------------------------
# Stage 5 — Review Loop  (imported from agents/)
# ---------------------------------------------------------------------------
# review_loop is a LoopAgent(ReviewCycle: Critic → Revisor)

# ---------------------------------------------------------------------------
# Stage 6 — Final Editing
# ---------------------------------------------------------------------------
final_editor = LlmAgent(
    name="FinalEditor",
    model="gemini-2.5-flash",
    instruction=FINAL_EDITOR_INSTRUCTION,
    description="Polishes the article into its publication-ready form.",
    output_key=KEY_FINAL_CONTENT,
)

# ---------------------------------------------------------------------------
# Root Agent — Full Pipeline
# ---------------------------------------------------------------------------
root_agent = SequentialAgent(
    name="ContentCreationPipeline",
    sub_agents=[
        topic_analyzer,       # 1. Plan
        parallel_research,    # 2. Research (parallel)
        parallel_content,     # 3. Write + Code (parallel)
        content_synthesizer,  # 4. Merge
        review_loop,          # 5. Review (loop)
        final_editor,         # 6. Polish
    ],
    description=(
        "End-to-end content creation pipeline that researches a topic, "
        "generates creative and technical content with code examples, "
        "iteratively reviews and revises, then polishes the final output."
    ),
)
