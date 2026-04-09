"""Web search tool using SerpAPI for the Research Agent."""

import os
from typing import Any

import requests

# Type alias for the search result structure.
# Each result dict contains: {"status": str, "results": list[dict], "error_message"?: str}
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
                "SERPAPI_KEY not set. Please add it to your .env file. "
                "Returning a simulated result for demo purposes."
            ),
            "results": [
                {
                    "title": f"Simulated result for: {query}",
                    "link": "https://example.com",
                    "snippet": (
                        f"This is a simulated search result for '{query}'. "
                        "Set SERPAPI_KEY in your .env to get real results."
                    ),
                }
            ],
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
