# CONTEXT.md — `frontend/`

React 18 + Vite UI. Proxies `/api` → `http://localhost:8000` (see `vite.config.js`).

## Files
- `package.json` — `dev` (vite :5173), `build` (vite build). Deps: react, react-dom, @vitejs/plugin-react, vite.
- `vite.config.js:1` — react plugin + proxy. No app logic.
- `index.html` — mounts `#root` → `src/main.jsx`.

## Subdirs
- `src/` — see `src/CONTEXT.md`. Rule: no fetch outside `src/api/`, no shared state outside `src/hooks/`.
