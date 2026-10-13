"""Orchestrate parser -> planner -> executor, plus resume. Delegates everything."""
import json
from sqlalchemy.orm import Session
from backend.agent.parser import parse_goal
from backend.agent.planner import make_plan
from backend.agent.executor import execute_step
from backend.agent.memory import save_fact, get_facts
from backend.agent.verifier import verify_run
from backend.agent.tools.registry import build_tools
from backend.config import settings
from backend.models.run import Run
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


def _save_step(db: Session, run: Run, n: int, res: dict, history: list) -> None:
    inside("_save_step", run.id)
    db.add(Step(run_id=run.id, n=n, thought=res["thought"][:4000],
                tool=res["tool"], args_json=json.dumps(res["args"]),
                obs=str(res["obs"])[:4000]))
    db.commit()
    # Emit step with n included for frontend
    _emit(run.id, {"type": "step", "n": n, "thought": res["thought"],
                   "tool": res["tool"], "args": res["args"],
                   "obs": res["obs"], "final": res["final"]})
    history.append({"n": n, "tool": res["tool"], "obs": str(res["obs"])[:1500]})


def _run_steps(db: Session, run: Run, goal: dict, plan: list,
               tools: dict | None, tool_schemas: list | None,
               history: list, skip: set = frozenset()) -> str:
    inside("_run_steps", run.id)
    final = ""
    for n, item in enumerate(plan[:settings.max_steps], 1):
        if n in skip:
            continue
        res = execute_step(goal, item, get_facts(db, run.id),
                           tool_schemas, tools, history)
        _save_step(db, run, n, res, history)
        if run.status == "waiting" or res["final"]:
            return res["obs"]
    if final == "" and run.status != "waiting":
        inside("_wrap_up", run.id)
        n = max([h["n"] for h in history] + [0]) + 1
        res = execute_step(goal, {"step": "Compile the deliverable the goal asked for from HISTORY, satisfying each success criterion with formatted results (no step numbers, no tool names). Reply FINAL: <deliverable>.", "tool": None}, get_facts(db, run.id), tool_schemas, tools, history)
        _save_step(db, run, n, res, history)
        if res["final"]:
            return res["obs"]
    return final


def _finish(db: Session, run: Run, final: str) -> dict:
    inside("_finish", run.id)
    if run.status == "waiting":
        _emit(run.id, {"type": "paused", "final": final, "status": run.status})
        return {"run_id": run.id, "final": final, "status": run.status,
                "verified": False, "evidence": ""}
    verdict = verify_run(db, run.id)
    set_status(db, run.id, "done" if verdict["verified"] else "failed")
    _emit(run.id, {"type": "done", "final": final, "status": run.status,
                   "verified": verdict["verified"],
                   "evidence": verdict["evidence"]})
    return {"run_id": run.id, "final": final, "status": run.status,
            "verified": verdict["verified"], "evidence": verdict["evidence"]}


def run_task(db: Session, task: str, tools: dict | None = None,
             tool_schemas: list | None = None, run_id: str | None = None) -> dict:
    inside("run_task", task)
    if run_id is None:
        run = create_run(db, task)
    else:
        run = db.query(Run).filter_by(id=run_id).one()
    if tools is None and tool_schemas is None:
        tools, tool_schemas = build_tools(db, run.id)
    goal = parse_goal(task)
    save_fact(db, run.id, "objective", goal["objective"])
    save_fact(db, run.id, "success_criteria", json.dumps(goal["success_criteria"]))
    _emit(run.id, {"type": "goal", "goal": goal})
    plan = make_plan(goal, sorted((tools or {}).keys()))
    run.plan_json = json.dumps(plan)
    db.commit()
    _emit(run.id, {"type": "plan", "plan": plan})
    out = _finish(db, run, _run_steps(db, run, goal, plan, tools, tool_schemas, []))
    out.update({"goal": goal, "plan": plan})
    return out


def resume_task(db: Session, run_id: str, tools: dict | None = None,
                tool_schemas: list | None = None) -> dict:
    inside("resume_task", run_id)
    run = db.query(Run).filter_by(id=run_id).one()
    if tools is None and tool_schemas is None:
        tools, tool_schemas = build_tools(db, run_id)
    facts = get_facts(db, run_id)
    try:
        criteria = json.loads(facts.get("success_criteria", "[]"))
    except ValueError:
        criteria = []
    goal = {"objective": facts.get("objective", run.task),
            "success_criteria": criteria}
    plan = json.loads(run.plan_json or "[]")
    steps = db.query(Step).filter_by(run_id=run_id).order_by(Step.n).all()
    history = [{"n": s.n, "tool": s.tool, "obs": (s.obs or "")[:1500]} for s in steps]
    _emit(run_id, {"type": "resumed"})
    out = _finish(db, run, _run_steps(db, run, goal, plan, tools,
                                      tool_schemas, history, {s.n for s in steps}))
    out.update({"goal": goal, "plan": plan})
    return out
