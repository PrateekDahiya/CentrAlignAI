# CONTEXT.md — `backend/agent/prompts/`

One system prompt per file. No code.

## Planned (Phase 2)
- `parser_prompt.py` — goal-extraction prompt.
- `planner_prompt.py` — plan-steps prompt (forces tool names from registry).
- `executor_prompt.py` — ReAct step prompt (thought + tool call JSON).
- `verifier_prompt.py` — verification prompt (quote ERP row + PDF values, boolean verdict).

Rule: prompts never imported by routers/UI — only by their matching `agent/*.py`.
