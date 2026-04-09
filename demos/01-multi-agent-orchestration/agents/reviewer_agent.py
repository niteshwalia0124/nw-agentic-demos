"""Reviewer agents — critic and revisor for iterative refinement.

A ``SequentialAgent`` pairs a critic (who evaluates the draft) with a
revisor (who incorporates feedback).  This sequence is wrapped in a
``LoopAgent`` so the review cycle repeats for a configurable number of
iterations, progressively improving the content.
"""

from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent

from ..prompts.instructions import CRITIC_INSTRUCTION, REVISOR_INSTRUCTION

# --- Configuration ---
MAX_REVIEW_ITERATIONS = 2

# --- State Keys ---
KEY_REVIEW_FEEDBACK = "review_feedback"
KEY_MERGED_DRAFT = "merged_draft"  # read and overwritten by the revisor

# --- Individual Agents ---

critic_agent = LlmAgent(
    name="ContentCritic",
    model="gemini-2.5-flash",
    instruction=CRITIC_INSTRUCTION,
    description=(
        "Reviews the current draft for clarity, accuracy, and "
        "engagement. Provides a rating and specific suggestions."
    ),
    output_key=KEY_REVIEW_FEEDBACK,
)

revisor_agent = LlmAgent(
    name="ContentRevisor",
    model="gemini-2.5-flash",
    instruction=REVISOR_INSTRUCTION,
    description=(
        "Revises the draft based on the critic's feedback, "
        "improving quality while maintaining structure."
    ),
    output_key=KEY_MERGED_DRAFT,  # overwrites merged_draft with revised version
)

# --- Review Cycle (Sequential: Critique → Revise) ---

review_cycle = SequentialAgent(
    name="ReviewCycle",
    sub_agents=[critic_agent, revisor_agent],
    description="Runs one critique-then-revise cycle.",
)

# --- Review Loop ---

review_loop = LoopAgent(
    name="ReviewLoop",
    sub_agents=[review_cycle],
    max_iterations=MAX_REVIEW_ITERATIONS,
    description=(
        f"Iteratively reviews and revises the draft "
        f"{MAX_REVIEW_ITERATIONS} times for quality improvement."
    ),
)
