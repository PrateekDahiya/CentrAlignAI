# CONTEXT.md — `data/inbox/`

Mock email-attachment inbox. PDFs are **generated fakes** (no real company data).

## Files
- `Acme_Corp_INV-1001.pdf` — $4,200.00, due 2026-10-20 (seed output, gitignored).
- `Acme_Corp_INV-1002.pdf` — $7,850.50, due 2026-11-05 (latest Acme → primary demo target).
- `Globex_INV-2001.pdf` — $1,230.00, due 2026-10-28.
- `.gitkeep` — keeps dir in git (PDFs ignored, regenerate via `python -m backend.seed.make_pdfs`).

Listed by `backend/routers/inbox_router.py:1`, parsed by `agent/tools/invoice_parse.py` (Phase 3).
