# CONTEXT.md — `backend/agent/`

Groq ReAct brain. **Phase 3 done** — real tools wired; full autonomous demo verified live: `file_list → invoice_parse → erp_create → erp_list` produced ERP row `INV-1002 $7850.50 2026-11-05`, status `done`.

## Files
- `groq_client.py:1` — `get_client()`, `chat(messages, primary, fallback, tools?, max_tokens?)`. Falls back on 429/rate errors only. gpt-oss requires `max_tokens>=1024` (default from `config.max_tokens=2048`).
- `parser.py:1` — `parse_goal(task)` → `{objective, success_criteria}` via planner model. Brace-tolerant `_extract_json`.
- `planner.py:1` — `make_plan(goal, tool_names)` → `[{step, tool|null, args_hint}]` (capped `max_steps`). Empty/invalid → single passthrough step.
- `executor.py:1` — `execute_step(goal, step_hint, facts, tool_schemas, tools, history?)` → `{thought, tool, args, obs, final}`. Dispatches `tools[name](**args)` with 3x retry on `RetryableError`; `TypeError`→bad-args, other→fatal. One corrective retry on Groq `tool_use_failed` (null args). No tool call + `FINAL:` prefix = done. Self-correct wrong-tool plans; ask only when data missing/options many; never repeat succeeded calls.
- `memory.py:1` — `save_fact` / `get_facts` on `facts` table. No LLM.
- `loop.py:1` — `run_task(db, task, tools?, tool_schemas?)`: create run → default `build_tools(db, run.id)` → parse → plan (`plan_json`) → execute with step HISTORY (fixes amnesia: without it executor re-parsed 3x, never wrote) → `steps` rows → break on `waiting` (ask_user pause) else `done`. `_emit` writes trace JSONL + best-effort SSE queue. Verdict logic arrives in Phase 5 (`verifier.py`).
- `__init__.py` — marker.

## Tool contract
`tools: dict[name, fn]` where `fn(**args_from_llm_json) -> str`. Schemas are OpenAI-function dicts in `tool_schemas`. See `tools/CONTEXT.md`.

## Subdirs
- `prompts/` — one system prompt per role (see `prompts/CONTEXT.md`).
- `tools/` — 8 real tools + `registry.py` (see `tools/CONTEXT.md`).
