# CONTEXT.md — `backend/agent/`

Groq ReAct brain. **Phase 2+ — currently placeholders only** (`__init__.py`). Do not put logic in `loop.py` alone; split per file below.

## Planned files (Phase 2/3/5)
- `loop.py` — orchestrate only: parser→planner→executor→verifier, `MAX_STEPS=12`.
- `parser.py` — NL task → `{objective, success_criteria}` (gpt-oss-120b).
- `planner.py` — goal → `steps[]` (120b, fallback qwen3.8-27b).
- `executor.py` — one step + 3x retry + fallback to gpt-oss-20b. `max_tokens>=2048` required.
- `verifier.py` — re-query MySQL+PDF via gpt-oss-20b → `{verified, evidence}` (fail-closed).
- `memory.py` — `facts` table CRUD wrapper.
- `prompts/` — one system-prompt file per role (see `prompts/CONTEXT.md`).
- `tools/` — one file per tool + `registry.py` (see `tools/CONTEXT.md`).
