# CONTEXT.md — `backend/agent/tools/`

One tool per file + registry. Contract: `fn(**args_from_llm_json) -> str`. **Phase 3 done** — 8 tools live-verified (parse seeds, ERP round-trip, pause gate, full invoice→ERP demo). Post-phase: `doc_text.py` added (PDF/image text) → 10 tools.

## Files
- `registry.py:1` — `build_tools(db, run_id)` → `(tools dict, schemas list)`. Binds session/run into `erp_*`/`ask_user` closures; pure tools passed direct. 10 tools, 10 schemas. Single import point for `loop.py`.
- `files.py:1` — `resolve()` (absolute or inbox-relative; must sit under `FILE_ROOTS` or inbox; `.env`/`.env.*` except `.env.example`, `*.pem`/`*.key`/`*id_rsa*` refused; bare `D:` normalized to drive root, trailing-sep prefix bug fixed live), `file_list()` (empty → inbox; missing → hint-only with inbox path, no misleading dump; outside → `refused:`), `file_read()` (PDFs → "use pdf_text/invoice_parse" hint, 4000 chars; missing → `not found:` without leaking abs paths).
- `doc_text.py:1` — `pdf_text(path, max_chars=6000)` via pdfplumber (empty → "try image_text" hint), `image_text(path)` OCR via pillow+pytesseract (auto-locates the Tesseract binary via PATH or Program Files; graceful "ocr unavailable" fallback otherwise). Guards: non-image → usage hint, missing → `not found:`, outside roots → `refused:`.
- `invoice_parse.py:1` — `invoice_parse(path)` via pdfplumber regex → `vendor= invoice_no= amount= due_date= source_file=`. Returns `unparsed:` when no match.
- `erp_tools.py:1` — `erp_list(db, vendor?)`, `erp_create(db, vendor, invoice_no, amount, due_date?, source_file?, source?)`. Idempotent on `invoice_no` (returns existing). `source` tags origin (`invoice` PDFs/files vs `web_search` prices); shown per row by `_fmt`. NOTE: `filter()` must precede `limit()` (SQLAlchemy rejects filter-after-limit — caught live).
- `web_search.py:1` — `web_search(query)`: Tavily if `TAVILY_API_KEY` set, else DuckDuckGo instant answer. Failures → `search failed:` string, never raise.
- `browser_open.py:1` — `browser_open(url)` Playwright Chromium headless (30s), real UA/viewport/locale, title + 3000 chars + screenshot to `runs/browser_<ts>.png`. Rejects non-http. Per-stage errors (`[launch/goto …]`), `finally: b.close()` (leaked browsers caused mystery launch failures live). Failures → `browser failed …` strings, never raise (needs `playwright install chromium`; missing binary was caught live).
- `ask_user.py:1` — `ask_user(db, run_id, question)` writes `facts(question)` + sets run `waiting`. Loop breaks; resume UX in Phase 4.
- `__init__.py` — marker.

## Hardening lessons (live)
- Groq rejects `null` for optional args (400 `tool_use_failed`) → executor prompt forbids null + one corrective retry in `execute_step`.
