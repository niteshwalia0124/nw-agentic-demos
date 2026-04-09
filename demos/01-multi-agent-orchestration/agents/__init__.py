"""Specialist agents for the Multi-Agent Orchestration demo.

Exports the composite agents that are used as stages in the main
pipeline defined in ``agent.py``.
"""

from .code_agent import code_agent
from .research_agent import parallel_research
from .reviewer_agent import review_loop
from .writer_agent import parallel_writers

__all__ = [
    "parallel_research",
    "code_agent",
    "parallel_writers",
    "review_loop",
]
