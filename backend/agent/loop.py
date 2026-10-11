"""Orchestrate parser -> planner -> executor. Delegates everything."""
import json
from sqlalchemy.orm import Session
from backend.agent.parser import parse_goal
from backend.agent.planner import make_plan
from backend.agent.executor import execute_step
from backend.agent.memory import save_fact, get_facts
from backend.config import settings
from backend.models.step import Step
from backend.services.run_service import create_run, set_status
from backend.services.trace_service import append_trace
from backend.utils.logging import inside


def _emit(run_id: str, event: dict) -> None:
    inside("_emit", run_id)
    append_trace(run_id, event)
    try:
        from backend.services.sse_service import get_queue
        get_queue(run_id).put_nowait(event)
    except Exception:
        pass


def run_task(db: Session, task: str, tools: dict | None = None,
             tool_schemas: list | None = None) -> dict:
    inside("run_task", task)
    run = create_run(db, task)
    _emit(run.id, {"type": "started", "task": task})
    goal = parse_goal(task)
    save_fact(db, run.id, "objective", goal["objective"])
    _emit(run.id, {"type": "goal", "goal": goal})
    plan = make_plan(goal, sorted((tools or {}).keys()))
    run.plan_json = json.dumps(plan)
    db.commit()
    _emit(run.id, {"type": "plan", "plan": plan})
    final = ""
    for n, item in enumerate(plan[:settings.max_steps], 1):
        res = execute_step(goal, item, get_facts(db, run.id), tool_schemas, tools)
        db.add(Step(run_id=run.id, n=n, thought=res["thought"][:4000],
                    tool=res["tool"], args_json=json.dumps(res["args"]),
                    obs=str(res["obs"])[:4000]))
        db.commit()
        _emit(run.id, {"type": "step", "n": n, "step": res})
        if res["final"]:
            final = res["obs"]
            break
    set_status(db, run.id, "done")
    _emit(run.id, {"type": "done", "final": final})
    return {"run_id": run.id, "goal": goal, "plan": plan, "final": final}
