"""One ReAct step: Groq tool call + dispatch + retry. No orchestration."""
import json
import time
from backend.agent.groq_client import chat
from backend.agent.prompts.executor_prompt import EXECUTOR_SYSTEM
from backend.config import settings
from backend.utils.errors import RetryableError
from backend.utils.logging import inside


def _call_tool(tools: dict, name: str, args: dict, retries: int = 3) -> str:
    inside("_call_tool", name)
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
                 tool_schemas: list | None, tools: dict | None,
                 history: list | None = None) -> dict:
    inside("execute_step", str((step_hint or {}).get("tool", "-")))
    ctx = (f"GOAL: {json.dumps(goal)}\nSTEP: {json.dumps(step_hint)}\n"
           f"FACTS: {json.dumps(facts)}\nHISTORY: {json.dumps(history or [])}")
    msgs = [{"role": "system", "content": EXECUTOR_SYSTEM},
            {"role": "user", "content": ctx}]
    try:
        res = chat(msgs, primary=settings.executor_model,
                   fallback=settings.executor_fallback, tools=tool_schemas)
    except Exception as e:
        if "tool_use_failed" not in str(e) and "400" not in str(e):
            return {"thought": "", "tool": "", "args": {},
                    "obs": f"llm error: {e}", "final": False}
        inside("execute_step_retry", str((step_hint or {}).get("tool", "-")))
        msgs.append({"role": "user", "content": "Last tool call rejected "
                     "(null/wrong args). Retry: omit optional args, never null."})
        try:
            res = chat(msgs, primary=settings.executor_model,
                       fallback=settings.executor_fallback, tools=tool_schemas)
        except Exception as e2:
            return {"thought": "", "tool": "", "args": {},
                    "obs": f"llm error: {e2}", "final": False}
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
