# CentrAlignAI — Autonomous AI Task Worker (Prototype)

User gives a natural-language task → Groq-powered ReAct agent plans, uses tools (files, PDFs, browser, mock ERP), writes to MySQL, verifies, and the React UI streams steps + evidence.

> Docs live with code: every directory has a `CONTEXT.md` explaining its files. **This README and all `CONTEXT.md` are updated after every phase** (see Phase status at bottom).

## Stack used

| Layer | Choice | Why |
|---|---|---|
| Agent brain | Groq API, `openai/gpt-oss-120b` (planner/executor) + `openai/gpt-oss-20b` (verifier/fast), fallback `qwen/qwen3.8-27b` | Free tier, OpenAI-compatible tool calling (verified live). Llama models retired on this key Sep 2026, so gpt-oss is used. `max_tokens>=2048` required (reasoning tokens else empty reply). |
| Backend | Python 3.12, FastAPI, Uvicorn, SQLAlchemy + PyMySQL | Thin routers, small files (max 31 lines), easy to debug live |
| DB | MySQL on Aiven (`centralign`, SSL, port 17886) | Tables: `runs`, `steps`, `facts` (memory), `erp_invoices` (`invoice_no` UNIQUE) |
| PDF | pdfplumber (parse) + reportlab (generate fake invoices) | Real extraction, mock data only |
| Browser | Playwright Chromium (Phase 3) | Real execution for web task |
| Frontend | React 18 + Vite, proxied `/api` | `api/` (fetch) / `hooks/` (state) / `components/` (presentational) split |
| Streaming | SSE (`sse-starlette`, `EventSource`) | Live thought/tool/obs + approval gate |
| Tests | pytest | Per-file: planner, retry, verifier, idempotency |

## Architecture

```
[React :5173] task box → POST /api/runs → SSE /api/runs/{id}/events → approval modal → evidence card
      │
[FastAPI :8000] routers/ (erp, inbox, runs, approval, events, trace) → services/ (run, sse, trace)
      │
[agent/] parser → planner (120b) → executor+tools (registry) → memory (facts) → verifier (20b, fail-closed)
      │  tools: web_search, browser_open, file_list/read, invoice_parse, erp_create/list, ask_user
[MySQL Aiven] runs / steps / facts / erp_invoices  +  runs/<id>/trace.jsonl mirror (--replay safe)
```

Human gate: `ask_user` sets run `waiting`; UI approves via `POST /api/runs/{id}/approve` → resumes. Verifier re-reads MySQL+PDF and returns `{verified, evidence}` — never marks done on hallucination.

## Setup

```powershell
# 1. clone + python deps
git clone <repo-url> CentrAlignAI; cd CentrAlignAI
pip install -r requirements.txt

# 2. env (NEVER commit .env)
copy .env.example .env
# edit .env: GROQ_API_KEY, DB_HOST/PORT/NAME/USERNAME/PASSWORD, models (see .env.example)

# 3. DB + seed inbox PDFs
python -m backend.seed.seed_db
python -m backend.seed.make_pdfs   # → data/inbox/*.pdf

# 4. frontend deps
cd frontend; npm install; cd ..
```

## Run (dev)

```powershell
# terminal 1 — backend (from repo root, .env loaded)
uvicorn backend.main:app --port 8000 --reload

# terminal 2 — frontend
cd frontend; npm run dev   # → http://localhost:5173
```

Smoke check:
```powershell
curl http://localhost:8000/api/health          # {"ok":true}
curl http://localhost:8000/api/inbox/files     # 3 pdfs
curl http://localhost:8000/api/erp/invoices    # []
```

## Build (prod demo)

```powershell
cd frontend; npm run build; cd ..   # → frontend/dist/ (serve via static or nginx)
# backend stays: uvicorn backend.main:app --port 8000
pytest -q                            # Phase 5+
```

## Key technical decisions

1. **Custom ReAct loop, not LangGraph/CrewAI** — own the autonomy logic, explainable in viva, per-file (`parser/planner/executor/verifier`).
2. **Dual Groq models (120b + 20b)** — 120b for reliable multi-step tool calling, 20b for cheap verify/summarize; saves TPM quota (12K limit), fallback chain on 429.
3. **MySQL with `invoice_no UNIQUE`** — idempotent ERP writes; re-runs don't duplicate.
4. **Small-files rule (<250 lines, actual max 31)** — `CONTEXT.md` per dir; any viva question maps to one file.
5. **Trace in DB + JSONL** — `steps` table + `runs/<id>/trace.jsonl` enables replay without LLM (quota-safe demo).

## Demo tasks (generalization on same 7 tools)

1. *"Find latest Acme invoice, extract amount/due date, enter into ERP"* → `Acme_Corp_INV-1002.pdf` → ERP row.
2. *"Web price → save file + log ERP"* (Phase 3+).
3. *"Pay invoice #999 (missing)"* → detect fail → retry → `ask_user`, never hallucinate.

## Known limitations

- SSE `events_router` is placeholder (Phase 4 streams real steps).
- `agent/` is scaffold only (Phase 2/3 implement loop + tools).
- `ApprovalModal`/`EvidenceCard` minimal (Phase 4 enriches).
- gpt-oss needs large `max_tokens`; 429 fallback to qwen not yet wired (Phase 2).
- No auth, no pagination, mock data only.

## What next (post-deadline)

- Phase 2–5 per `CONTEXT.md` Phase status; demo video (3–4 min: Task1 success + Task3 gate + MySQL row + trace); `pytest` suite; `--replay` offline mode.

## Assumptions

- Groq free tier suffices (30 RPM); Aiven MySQL reachable with SSL; mock PDFs stand in for email inbox; no real credentials/data.

## Phase status (updated each phase)

- [x] Phase 0: scaffold, config, SSL engine, React shell
- [x] Phase 1: MySQL tables, seed PDFs, ERP/inbox/runs APIs verified (+ CONTEXT.md + README)
- [ ] Phase 2: Groq ReAct brain
- [ ] Phase 3: tools
- [ ] Phase 4: SSE + approval UI
- [ ] Phase 5: verifier + tests
- [ ] Phase 6: packaging + video + submission (Oct 14, 11:30 AM IST)
