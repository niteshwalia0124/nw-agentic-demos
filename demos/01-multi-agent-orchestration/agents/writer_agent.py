"""Writer agents — creative and technical content drafters.

Two writers with different ``temperature`` settings run in parallel via a
``ParallelAgent``.  The creative writer aims for engagement while the
technical writer focuses on accuracy.  Both write to separate state keys
so the downstream synthesiser can merge them.
"""

from google.adk.agents import LlmAgent, ParallelAgent
from google.genai import types

from ..prompts.instructions import (
    CREATIVE_WRITER_INSTRUCTION,
    TECHNICAL_WRITER_INSTRUCTION,
)

# --- Configuration ---
MAX_WORDS = 300

# --- State Keys ---
KEY_CREATIVE_DRAFT = "creative_draft"
KEY_TECHNICAL_DRAFT = "technical_draft"

# --- Individual Writer Agents ---

creative_writer = LlmAgent(
    name="CreativeWriter",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0.8),
    instruction=CREATIVE_WRITER_INSTRUCTION.format(max_words=MAX_WORDS),
    description=(
        "Writes an engaging, reader-friendly content draft using "
        "vivid analogies and storytelling. High temperature for creativity."
    ),
    output_key=KEY_CREATIVE_DRAFT,
)

technical_writer = LlmAgent(
    name="TechnicalWriter",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0.3),
    instruction=TECHNICAL_WRITER_INSTRUCTION.format(max_words=MAX_WORDS),
    description=(
        "Writes a precise, detailed technical content draft. "
        "Low temperature for accuracy and consistency."
    ),
    output_key=KEY_TECHNICAL_DRAFT,
)

# --- Parallel Writing Phase ---

parallel_writers = ParallelAgent(
    name="ParallelWriters",
    sub_agents=[creative_writer, technical_writer],
    description="Runs creative and technical writers in parallel.",
)
