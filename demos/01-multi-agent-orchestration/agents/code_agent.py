"""Code Agent — writes clean, documented code examples.

Uses a low ``temperature`` via ``GenerateContentConfig`` to produce
precise, deterministic code.  Output is persisted to shared state with
``output_key`` so other agents can embed the code in the final article.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ..prompts.instructions import CODE_WRITER_INSTRUCTION

# --- State Key ---
KEY_CODE_EXAMPLES = "code_examples"

code_agent = LlmAgent(
    name="CodeExampleWriter",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0.3),
    instruction=CODE_WRITER_INSTRUCTION,
    description=(
        "Writes clean, well-documented Python code examples that "
        "illustrate the topic. Uses low temperature for precision."
    ),
    output_key=KEY_CODE_EXAMPLES,
)
