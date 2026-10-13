# DEPLOY — Render (Blueprint)

## One-time setup (5 min + build time)

1. Push latest `main` (this repo already contains `Dockerfile` + `render.yaml`).
2. Render dashboard → **New → Blueprint** → select this repo.
3. Fill the `sync: false` secrets when prompted: `GROQ_API_KEY`,
   `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD` (same values as local `.env`).
4. Deploy. Render builds the API image (Python + Chromium + Tesseract)
   and the UI static site, wiring `VITE_API_URL` automatically.

## After deploy

- API: `https://taskpilot-api.onrender.com/api/health` → `{"ok":true}`
- UI: `https://taskpilot-ui.onrender.com` — run the smoke trio from `INSTALL.md`
  (invoice→ERP, ERP list, resume-style file task via inbox).
- MySQL (Aiven) is shared with local dev — already seeded, nothing to migrate
  (the `source` column was added live; fresh DBs get it via `create_all`).

## Know before demo day

- **Cold starts**: free web services sleep when idle; first click after
  idleness takes ~30–60s. Starter ($7/mo) stays warm.
- **Ephemeral disk**: `runs/*.png` screenshots and regenerated inbox PDFs vanish
  on restart/redeploy. The `steps` table already mirrors every trace, so no
  evidence is load-bearing on disk. Re-seed inbox PDFs any time with
  `python -m backend.seed.make_pdfs` (needs repo checkout, not the container).
- **Sandbox story**: no `FILE_ROOTS` in the cloud — file tools are scoped to
  `data/inbox`, which is the correct least-privilege posture for evaluators.
- **CORS** is `*` (demo). Lock it to the UI origin in `backend/main.py`
  if time allows before submission.
