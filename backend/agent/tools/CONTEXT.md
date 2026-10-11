# CONTEXT.md — `backend/agent/tools/`

One tool per file + registry. Each returns `{ok, data, error}`, timeout 30s.

## Planned (Phase 3)
- `registry.py` — `TOOL_MAP` + OpenAI-function schemas for Groq `tools=` param.
- `web_search.py` — Tavily/DDG fallback.
- `browser_open.py` — Playwright headless → text + screenshot to `runs/`.
- `files.py` — `file_list`, `file_read` for `data/inbox/`.
- `invoice_parse.py` — pdfplumber amount/due-date regex.
- `erp_tools.py` — `erp_create`, `erp_list` via MySQL.
- `ask_user.py` — sets run `waiting`, pauses loop until `approval_router` resumes.
