# CONTEXT.md — `backend/routers/`

Thin HTTP endpoints. Each file one router; no LLM, no business rules beyond idempotency.

## Files
- `erp_router.py:1` — `GET /api/erp/invoices` (last 100), `POST /api/erp/invoices` (on `IntegrityError` returns existing row by `invoice_no` — idempotent).
- `inbox_router.py:1` — `GET /api/inbox/files` lists `data/inbox/*.pdf` basenames. Returns `[]` if dir missing.
- `runs_router.py:1` — `POST /api/runs` (creates `Run` uuid, status `running`), `GET /api/runs/{id}`.
- `approval_router.py:1` — `POST /api/runs/{id}/approve` writes `facts(user_approval)` + sets `running`/`cancelled`.
- `events_router.py:1` — `GET /api/runs/{id}/events` SSE placeholder (Phase 4 → real step stream via `sse_service`).
- `trace_router.py:1` — `GET /api/runs/{id}/trace` returns `runs/<id>/trace.jsonl` or `{steps:[]}`.
- `__init__.py` — marker.
