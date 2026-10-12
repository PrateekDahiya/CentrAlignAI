# CONTEXT.md — `backend/routers/`

Thin HTTP endpoints. Each file one router; no LLM, no business rules beyond idempotency.

## Files
- `erp_router.py:1` — `GET /api/erp/invoices` (last 100), `POST /api/erp/invoices` (on `IntegrityError` returns existing row by `invoice_no` — idempotent).
- `inbox_router.py:1` — `GET /api/inbox/files` lists `data/inbox/*.pdf` basenames. Returns `[]` if dir missing.
- `runs_router.py:1` — `POST /api/runs` creates `Run` + launches `_execute` (own session → `run_task(run_id=...)`) via BackgroundTasks, returns immediately. `GET /api/runs` lists last 50 (`RunListOut`). `GET /api/runs/{id}`.
- `approval_router.py:1` — `POST /api/runs/{id}/approve` writes `facts(user_approval)` + sets `running`/`cancelled`; on approve schedules `_resume` (own session → `resume_task`). Decline does not resume.
- `events_router.py:1` — `GET /api/runs/{id}/events` SSE tailed from `runs/<id>/trace.jsonl` (0.5s poll, ends on `done`, 120s idle timeout). File tail, NOT the in-memory queue: `asyncio.Queue.put_nowait` from worker threads never wakes the server loop, so the queue stays empty (caught live).
- `status_router.py:1` — `GET /api/runs/{id}/status` → `{status, question}` (latest `facts(question)`), for UI polling.
- `trace_router.py:1` — `GET /api/runs/{id}/trace` returns `runs/<id>/trace.jsonl` or `{steps:[]}`.
- `__init__.py` — marker.
