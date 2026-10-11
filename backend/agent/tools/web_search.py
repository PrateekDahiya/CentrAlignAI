"""Web search: Tavily if key set, else DuckDuckGo instant answer."""
import os
import requests
from backend.utils.logging import inside


def _tavily(q: str) -> str:
    key = os.getenv("TAVILY_API_KEY", "")
    if not key:
        return ""
    r = requests.post("https://api.tavily.com/search",
                      json={"api_key": key, "query": q, "max_results": 3},
                      timeout=15).json()
    return "\n".join(f"- {x.get('title')}: {x.get('content', '')[:300]}"
                     for x in r.get("results", []))


def _ddg(q: str) -> str:
    r = requests.get("https://api.duckduckgo.com/",
                     params={"q": q, "format": "json", "no_html": 1},
                     timeout=15).json()
    lines = []
    if r.get("AbstractText"):
        lines.append(r["AbstractText"][:500])
    for t in (r.get("RelatedTopics") or [])[:3]:
        if isinstance(t, dict) and t.get("Text"):
            lines.append(t["Text"][:300])
    return "\n".join(f"- {x}" for x in lines)


def web_search(query: str = "") -> str:
    inside("web_search", query)
    if not query:
        return "error: query required"
    try:
        out = _tavily(query) or _ddg(query)
    except Exception as e:
        return f"search failed: {e}"
    return "results:\n" + out if out else "results: (none)"


SCHEMAS = [
    {"type": "function", "function": {
        "name": "web_search",
        "description": "Search the web for facts, prices, or pages",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"}}, "required": ["query"]}}},
]
