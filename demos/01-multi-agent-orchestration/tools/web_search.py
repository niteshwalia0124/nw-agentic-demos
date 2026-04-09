"""Web search utility (legacy).

This module is retained for backward compatibility.  The recommended
approach is to use ADK's built-in ``google_search`` tool which is
configured in the research agents::

    from google.adk.tools import google_search

If you need a standalone search function (e.g. for testing without
a Gemini API key), you can still use the ``web_search`` function
below with a SerpAPI key.
"""

import os
from typing import Any

import requests

# Type alias for the search result structure.
SearchResult = dict[str, Any]


def web_search(query: str) -> SearchResult:
    """Search the web using SerpAPI and return the top results.

    Args:
        query: The search query string.

    Returns:
        A dictionary containing the search status and a list of results,
        each with a title, link, and snippet.
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": (
                "SERPAPI_KEY not set. The primary search tool is ADK's "
                "built-in google_search — this legacy function requires "
                "a SerpAPI key."
            ),
            "results": [],
        }

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "q": query,
                "api_key": api_key,
                "engine": "google",
                "num": 5,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic_results", [])[:5]:
            results.append(
                {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                }
            )

        return {"status": "success", "results": results}
    except requests.RequestException as e:
        return {"status": "error", "error_message": str(e), "results": []}
