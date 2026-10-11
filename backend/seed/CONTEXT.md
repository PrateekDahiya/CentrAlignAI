# CONTEXT.md — `backend/seed/`

One-off setup scripts. Run manually, never from app startup.

## Files
- `make_pdfs.py:1` — `make_pdfs()` writes 3 fake invoices via reportlab to `data/inbox/`: `Acme_Corp_INV-1001.pdf` ($4,200.00, 2026-10-20), `Acme_Corp_INV-1002.pdf` ($7,850.50, 2026-11-05), `Globex_INV-2001.pdf` ($1,230.00, 2026-10-28). Run: `python -m backend.seed.make_pdfs`.
- `seed_db.py:1` — `init_db()` imports all models + `Base.metadata.create_all(engine)`. Run with DB env set. Does NOT insert rows (ERP rows created via API/agent to prove execution).
- `__init__.py` — marker.
