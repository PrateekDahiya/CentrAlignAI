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
- No file >250 lines (current max 31). One responsibility per file.
- `CONTEXT.md` in every directory, updated after each phase.
- No secrets in git. No real company data — mock PDFs only.

## Phase status
- [x] Phase 0: scaffold, config, SSL engine, React shell
- [x] Phase 1: MySQL tables, seed PDFs, ERP/inbox/runs APIs verified
- [ ] Phase 2: Groq ReAct brain (`backend/agent/`)
- [ ] Phase 3: tools
- [ ] Phase 4: SSE streaming + approval UI wiring
- [ ] Phase 5: verifier + tests
- [ ] Phase 6: packaging + demo video + submission
