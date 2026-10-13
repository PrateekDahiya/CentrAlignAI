# CONTEXT.md — `backend/agent/prompts/`

One system prompt per file. No code. **Phase 2 done** (verifier prompt ready for Phase 5).

## Files
- `parser_prompt.py:1` — `PARSER_SYSTEM`: one JSON object `{objective, success_criteria}`, `ASK USER:` criterion when ambiguous.
- `planner_prompt.py:1` — `PLANNER_SYSTEM`: one JSON array of `{step, tool|null, args_hint}`. NOTE: literal braces are doubled (`{{}}`) — file is `.format()`ed with `{tools}`/`{max_steps}` in `planner.py` (a `KeyError: '"step"'` bug caught live in Phase 2 smoke).
- `executor_prompt.py:1` — `EXECUTOR_SYSTEM`: call one tool per step, or reply `FINAL: <summary>`. Never invent data; act over ask (ask only when data missing/options many); reuse HISTORY, never repeat succeeded calls; never pass null args. FINAL must be the deliverable itself (criteria satisfied, formatted, no step narration).
- `verifier_prompt.py:1` — `VERIFIER_SYSTEM`: one JSON `{verified, evidence}`, fail-closed (Phase 5).

Rule: prompts imported only by their matching `agent/*.py`.
