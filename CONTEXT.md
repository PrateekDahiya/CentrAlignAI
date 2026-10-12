# CONTEXT.md — Repo Root (CentrAlignAI)

Autonomous AI Task Worker prototype. User gives NL task → Python agent loop (Groq) uses tools → writes to MySQL (Aiven) → React UI shows live steps + evidence.

## Directories
- `backend/` — FastAPI app + agent. See `backend/CONTEXT.md`.
- `frontend/` — React Vite UI. See `frontend/CONTEXT.md`.
- `data/inbox/` — Generated fake invoice PDFs (seed output). See `data/inbox/CONTEXT.md`.
- `runs/` — (gitignored) per-run `trace.jsonl` mirrors. Created at runtime.

## Key files here
- `requirements.txt` — pinned Python deps (fastapi, uvicorn, groq, sqlalchemy, pymysql, pdfplumber, reportlab, playwright, pytest, sse-starlette).
- `.env.example` — placeholder env (models, DB fields). Copy to `.env` locally. NEVER commit `.env`.
- `.gitignore` — ignores `.env`, `.venv/`, `__pycache__/`, `runs/`, `*.db`, `data/inbox/*.pdf` (keeps `.gitkeep`), `frontend/node_modules/`, `frontend/dist/`.
- `README.md` — setup/run/build, stack, architecture. Updated after every phase.
- `backend/main.py:1` — FastAPI wiring only.

## Conventions (enforced)
- No file >250 lines (current max 109). One responsibility per file.
- Logging: `inside {method} for {identifier}` as first line of every method (backend `inside()`, frontend `console.info`).
- `CONTEXT.md` in every directory, updated after each phase.
- No secrets in git. No real company data — mock PDFs only.

## Phase status
- [x] Phase 0: scaffold, config, SSL engine, React shell
- [x] Phase 1: MySQL tables, seed PDFs, ERP/inbox/runs APIs verified
- [x] Phase 2: Groq ReAct brain (prompts, parser/planner/executor/loop, live echo-tool smoke verified)
- [x] Phase 3: tools (8 real tools + registry, loop wiring + waiting pause, live invoice→ERP demo verified)
- [x] Phase 4: SSE streaming + approval UI wiring
- [x] Phase 5: verifier (fail-closed verify_run, done/failed verdict, UI badge, live true/false paths verified)
- [ ] Phase 6: packaging + demo video + submission
