"""Goal -> ordered steps via Groq. No execution here."""
import json
from backend.agent.groq_client import chat
from backend.agent.prompts.planner_prompt import PLANNER_SYSTEM
from backend.config import settings


def make_plan(goal: dict, tool_names: list[str]) -> list[dict]:
    system = PLANNER_SYSTEM.format(tools=tool_names or ["(none yet)"],
                                   max_steps=settings.max_steps)
    res = chat(
        [{"role": "system", "content": system},
         {"role": "user", "content": json.dumps(goal)}],
        primary=settings.planner_model, fallback=settings.planner_fallback,
    )
    text = res.choices[0].message.content or ""
    try:
        plan = json.loads(text)
    except ValueError:
        start, end = text.find("["), text.rfind("]")
        try:
            plan = json.loads(text[start:end + 1]) if 0 <= start < end else []
        except ValueError:
            plan = []
    if not isinstance(plan, list) or not plan:
        return [{"step": goal.get("objective", ""), "tool": None, "args_hint": {}}]
    return plan[:settings.max_steps]
