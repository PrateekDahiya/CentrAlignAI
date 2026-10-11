# CONTEXT.md — `backend/utils/`

Tiny helpers. No imports from routers/agent (leaf modules).

## Files
- `ids.py:1` — `new_run_id()` uuid4 str.
- `errors.py:1` — `ToolError`, `RetryableError`, `FatalError` (executor retry policy keys off these).
- `logging.py:1` — `get_logger(run_id)` with correlation prefix + `inside(method, identifier)` entry helper. Format: `inside {method} for {identifier}` (identifier truncated to 80 chars). Call as first line of every method; identifier = `run_id` when available, else task/invoice_no/tool name/`"-"`. Frontend mirrors with `console.info` in `api/` + hooks.
- `__init__.py` — marker.
