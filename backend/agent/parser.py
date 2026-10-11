"""NL task -> goal JSON via Groq. No planning here."""
import json
from backend.agent.groq_client import chat
from backend.agent.prompts.parser_prompt import PARSER_SYSTEM
from backend.config import settings
from backend.utils.logging import inside


def _extract_json(text: str) -> dict:
    inside("_extract_json", text)
    try:
        return json.loads(text)
    except ValueError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        try:
            return json.loads(text[start:end + 1])
        except ValueError:
            pass
    return {}


def parse_goal(task: str) -> dict:
    inside("parse_goal", task)
    res = chat(
        [{"role": "system", "content": PARSER_SYSTEM},
         {"role": "user", "content": task}],
        primary=settings.planner_model, fallback=settings.planner_fallback,
    )
    goal = _extract_json(res.choices[0].message.content or "")
    return {
        "objective": goal.get("objective") or task,
        "success_criteria": goal.get("success_criteria") or [],
    }
