# CONTEXT.md — `backend/services/`

Non-HTTP helpers. No LLM calls.

## Files
- `run_service.py:1` — `create_run(db,task)`, `set_status(db,run_id,status)`. DB writes only.
- `sse_service.py:1` — in-memory `asyncio.Queue` per `run_id`; `get_queue()`, `publish()`. Phase 4 wiring to `events_router`.
- `trace_service.py:1` — `append_trace(run_id,event)` appends JSON line to `runs/<run_id>/trace.jsonl` (gitignored). Used by agent loop + for `--replay` offline demo.
- `__init__.py` — marker.
