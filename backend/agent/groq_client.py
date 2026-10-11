"""Groq client + 429 fallback. No prompts, no tools."""
from groq import Groq
from backend.config import settings
from backend.utils.logging import inside

_client: Groq | None = None


def get_client() -> Groq:
    inside("get_client", "-")
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key or None)
    return _client


def chat(messages: list, *, primary: str, fallback: str, tools=None, max_tokens: int = 0):
    """One chat call. Falls back on rate limits. gpt-oss needs max_tokens>=1024."""
    inside("chat", primary)
    kw: dict = {"model": primary, "messages": messages,
                "max_tokens": max_tokens or settings.max_tokens}
    if tools:
        kw["tools"] = tools
        kw["tool_choice"] = "auto"
    try:
        return get_client().chat.completions.create(**kw)
    except Exception as e:
        if getattr(e, "status_code", 0) != 429 and "rate" not in str(e).lower():
            raise
        kw["model"] = fallback
        return get_client().chat.completions.create(**kw)
