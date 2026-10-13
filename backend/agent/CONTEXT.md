# CONTEXT.md — `backend/agent/`

Groq ReAct brain. **Phase 5 done** — fail-closed verification: `_finish` runs `verify_run` before terminal status (`done` if verified, `failed` otherwise, `paused` when waiting).

## Files
- `groq_client.py:1` — `get_client()`, `chat(messages, primary, fallback, tools?, max_tokens?)`. Falls back on 429/rate errors only. gpt-oss requires `max_tokens>=1024` (default from `config.max_tokens=2048`).
- `parser.py:1` — `parse_goal(task)` → `{objective, success_criteria}` via planner model. Brace-tolerant `_extract_json`.
- `planner.py:1` — `make_plan(goal, tool_names)` → `[{step, tool|null, args_hint}]` (capped `max_steps`). Empty/invalid → single passthrough step.
- `executor.py:1` — `execute_step(goal, step_hint, facts, tool_schemas, tools, history?)` → `{thought, tool, args, obs, final}`. Dispatches `tools[name](**args)` with 3x retry on `RetryableError`; `TypeError`→bad-args, other→fatal. One corrective retry on Groq `tool_use_failed` (null args). No tool call + `FINAL:` marker on any line (leading whitespace tolerated; obs = text after marker) = done. Self-correct wrong-tool plans; ask only when data missing/options many; never repeat succeeded calls.
- `memory.py:1` — `save_fact` / `get_facts` on `facts` table. No LLM.
- `verifier.py:1` — `verify_run(db, run_id)` → `{verified, evidence}`. Gathers objective/criteria + step obs (1500 chars/step — 400 truncated full tables and caused a false `failed` live) + ERP rows, judges via verifier model, saves `facts(verification)`. Fail-closed: parse/LLM error → False. ERP rows filtered to those referenced in step obs (unfiltered dump made the model parrot invoice rows as evidence for web tasks — caught live).
- `loop.py:1` — `run_task(...)` / `resume_task(...)` share `_run_steps` (HISTORY, skip-set, waiting break; `_save_step` helper) plus a `_wrap_up` final-answer attempt when the plan ends without FINAL, then `_finish` (verify → `done`/`failed`/`paused`, emits verdict).
- `__init__.py` — marker.

## Tool contract
`tools: dict[name, fn]` where `fn(**args_from_llm_json) -> str`. Schemas are OpenAI-function dicts in `tool_schemas`. See `tools/CONTEXT.md`.

## Subdirs
- `prompts/` — one system prompt per role (see `prompts/CONTEXT.md`).
- `tools/` — 10 real tools + `registry.py` (see `tools/CONTEXT.md`).
