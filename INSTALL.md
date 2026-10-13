# INSTALL — CentrAlignAI setup & run guide (Windows, PowerShell)

One-time setup, then two terminals to run. Every command is copy-paste ready.
Repo root in all commands: the folder containing `requirements.txt`.

## 0. Prerequisites

- Python 3.12 (`python --version`)
- Node.js 18+ (`node --version`) — frontend only
- MySQL reachable (Aiven credentials go into `.env` below)
- Git

## 1. Backend setup (once)

```powershell
# from repo root
pip install -r requirements.txt
python -m playwright install chromium   # browser tool engine (~170MB)
python third_party/fetch_tesseract.py  # image OCR engine (Windows; skips if present)

# environment (NEVER commit .env — it is gitignored)
copy .env.example .env
# edit .env: GROQ_API_KEY, DB_HOST/DB_PORT/DB_NAME/DB_USERNAME/DB_PASSWORD
# optional: FILE_ROOTS=D:/documents/Projects  (; separated — needs backend restart)
# optional: TESSERACT_CMD=C:\path\to\tesseract.exe  (else auto-detected)
# optional: TAVILY_API_KEY  (else web search uses DuckDuckGo fallback)

# database tables + mock invoice PDFs
python -m backend.seed.seed_db
python -m backend.seed.make_pdfs       # → data/inbox/*.pdf (gitignored)
```

## 2. Frontend setup (once)

```powershell
cd frontend
npm install
cd ..
```

## 3. Run (two terminals, every time)

```powershell
# terminal 1 — backend API (from repo root, .env auto-loaded)
uvicorn backend.main:app --port 8000 --reload
```

```powershell
# terminal 2 — frontend
cd frontend
npm run dev                            # → http://localhost:5173
```

## 4. Smoke check

```powershell
curl http://localhost:8000/api/health          # {"ok":true}
curl http://localhost:8000/api/inbox/files     # 3 pdfs
curl http://localhost:8000/api/erp/invoices    # []
```

UI flow: type a task → Run agent → live steps stream in → approval modal
pops if the agent needs input → Approve resumes, Decline cancels → verdict +
evidence card with trace download. Past runs live in the left panel.

## 5. Production build (demo packaging)

```powershell
cd frontend; npm run build; cd ..     # → frontend/dist/ (gitignored)
# backend stays: uvicorn backend.main:app --port 8000
```

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| `--reload` picked up code edits but not `.env` changes | `.env` loads once at import — stop + restart backend after editing it (same for new `FILE_ROOTS`) |
| `pip install` mentions gradio/starlette conflict | Pre-existing system-package clash, unrelated to this repo — ignore |
| `tesseract` not recognized in a new shell | Fresh installs need a reopened terminal for PATH; the app itself auto-detects via `TESSERACT_CMD` → `third_party/` → PATH → Program Files, no restart needed (lazy import) |
| `browser failed [launch …]` repeatedly | Kill orphan `chrome.exe`/`chromium` processes (old runs leaked them before the `finally: close` fix), then retry |
| Port 8000/5173 busy | Previous server still running — stop it or use `--port 8001` (+ update `vite.config.js` proxy) |
| OCR returns "ocr unavailable" | Run `python third_party/fetch_tesseract.py`, or `pip install pillow pytesseract` + native Tesseract binary |
| Fresh machine, Windows | `pip install -r requirements.txt` covers Python libs; the two native engines come from steps `playwright install chromium` + `fetch_tesseract.py` |
| Fresh machine, Linux/Mac | Playwright: `python -m playwright install chromium`; Tesseract: package manager install + `TESSERACT_CMD` in `.env` |
