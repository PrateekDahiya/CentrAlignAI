# CONTEXT.md — `backend/agent/`

Groq ReAct brain. **Phase 2 done** — parser→planner→executor→loop verified live with a fake echo tool (3 steps in MySQL, 7-line trace, tool actually dispatched).

## Files
- `groq_client.py:1` — `get_client()`, `chat(messages, primary, fallback, tools?, max_tokens?)`. Falls back on 429/rate errors only. gpt-oss requires `max_tokens>=1024` (default from `config.max_tokens=2048`).
- `parser.py:1` — `parse_goal(task)` → `{objective, success_criteria}` via planner model. Brace-tolerant `_extract_json`.
- `planner.py:1` — `make_plan(goal, tool_names)` → `[{step, tool|null, args_hint}]` (capped `max_steps`). Empty/invalid → single passthrough step.
- `executor.py:1` — `execute_step(goal, step_hint, facts, tool_schemas, tools)` → `{thought, tool, args, obs, final}`. Dispatches `tools[name](**args)` with 3x retry on `RetryableError`; `TypeError`→bad-args, other→fatal. No tool call + `FINAL:` prefix = done.
- `memory.py:1` — `save_fact` / `get_facts` on `facts` table. No LLM.
- `loop.py:1` — `run_task(db, task, tools?, tool_schemas?)`: create run → parse → plan (saved to `plan_json`) → execute steps (saved to `steps`) → status `done`. `_emit` writes trace JSONL + best-effort SSE queue. Verdict logic arrives in Phase 5 (`verifier.py`).
- `__init__.py` — marker.

## Tool contract (for Phase 3)
`tools: dict[name, fn]` where `fn(**args_from_llm_json) -> str|any`. Schemas are OpenAI-function dicts in `tool_schemas`.

## Subdirs
- `prompts/` — one system prompt per role (see `prompts/CONTEXT.md`).
- `tools/` — Phase 3 (real tools + `registry.py`).
