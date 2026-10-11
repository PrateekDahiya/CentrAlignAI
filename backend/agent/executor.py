"""One ReAct step: Groq tool call + dispatch + retry. No orchestration."""
import json
import time
from backend.agent.groq_client import chat
from backend.agent.prompts.executor_prompt import EXECUTOR_SYSTEM
from backend.config import settings
from backend.utils.errors import RetryableError


def _call_tool(tools: dict, name: str, args: dict, retries: int = 3) -> str:
    fn = (tools or {}).get(name)
    if fn is None:
        return f"unknown tool: {name}"
    if not isinstance(args, dict):
        args = {}
    last = "tool failed"
    for i in range(retries):
        try:
            return str(fn(**args))
        except RetryableError as e:
            last = f"retryable error ({i + 1}/{retries}): {e}"
            time.sleep(1 + i)
        except TypeError as e:
            return f"bad args for {name}: {e}"
        except Exception as e:
            return f"fatal tool error: {e}"
    return last


def execute_step(goal: dict, step_hint: dict, facts: dict,
                 tool_schemas: list | None, tools: dict | None) -> dict:
    ctx = f"GOAL: {json.dumps(goal)}\nSTEP: {json.dumps(step_hint)}\nFACTS: {json.dumps(facts)}"
    res = chat(
        [{"role": "system", "content": EXECUTOR_SYSTEM},
         {"role": "user", "content": ctx}],
        primary=settings.executor_model, fallback=settings.executor_fallback,
        tools=tool_schemas,
    )
    msg = res.choices[0].message
    thought = msg.content or getattr(msg, "reasoning", "") or ""
    calls = msg.tool_calls or []
    if not calls:
        return {"thought": thought, "tool": "", "args": {},
                "obs": thought, "final": thought.startswith("FINAL:")}
    outs, used, last_args = [], "", {}
    for tc in calls:
        name = tc.function.name
        try:
            last_args = json.loads(tc.function.arguments or "{}")
        except ValueError:
            last_args = {}
        used = name
        outs.append(f"{name} -> {_call_tool(tools, name, last_args)}")
    return {"thought": thought, "tool": used, "args": last_args,
            "obs": "\n".join(outs), "final": False}
