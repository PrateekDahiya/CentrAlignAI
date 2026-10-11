# CONTEXT.md — `backend/`

Python FastAPI backend. Entry `main.py` only wires routers (no logic).

## Files
- `main.py:1` — creates `FastAPI`, CORS `*`, mounts all routers, `GET /api/health`. No business logic.
- `config.py:1` — `Settings` dataclass from `.env`. Defaults: planner/executor `openai/gpt-oss-120b`, fallback `qwen/qwen3.8-27b` / `openai/gpt-oss-20b`, verifier `openai/gpt-oss-20b`, `MAX_STEPS=12`. NOTE: Llama models unavailable on this Groq key (retired Sep 2026); gpt-oss needs `max_tokens>=1024` (reasoning tokens else empty reply).
- `__init__.py` — package marker.

## Subdirs (each has own CONTEXT.md)
- `db/` — engine (Aiven SSL), Base, session dependency.
- `models/` — SQLAlchemy tables: `runs`, `steps`, `facts`, `erp_invoices`.
- `schemas/` — Pydantic request/response DTOs.
- `routers/` — thin HTTP endpoints, delegate to services/DB.
- `services/` — DB ops, SSE queues, trace writer. No LLM.
- `agent/` — (Phase 2+) Groq ReAct loop. Currently only `__init__.py` placeholders.
- `utils/` — ids, errors, logging helpers.
- `seed/` — `make_pdfs.py` (fake PDFs), `seed_db.py` (`create_all`).

## Rules
- Routers never call Groq directly. Agent never touches HTTP layer.
- Import direction: routers → services/models/schemas, agent → config/db/tools.
