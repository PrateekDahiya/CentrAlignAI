# CONTEXT.md — `frontend/src/`

UI entry + composition. No data fetching here.

## Files
- `main.jsx:1` — `createRoot` → `<App/>`.
- `App.jsx:1` — layout only: sidebar (`RunHistory`) + main (`TaskForm`, `StepList`, approval). `viewId` switches displayed run; submit resets to live.

## Subdirs
- `api/` — fetch/SSE wrappers only.
- `hooks/` — React state only.
- `components/` — presentational only (props in, no direct fetch).
