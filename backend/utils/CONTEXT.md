# CONTEXT.md — `backend/utils/`

Tiny helpers. No imports from routers/agent (leaf modules).

## Files
- `ids.py:1` — `new_run_id()` uuid4 str.
- `errors.py:1` — `ToolError`, `RetryableError`, `FatalError` (executor retry policy keys off these).
- `logging.py:1` — `get_logger(run_id)` with correlation prefix.
- `__init__.py` — marker.
