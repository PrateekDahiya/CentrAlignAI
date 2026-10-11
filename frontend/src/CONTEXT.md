# CONTEXT.md — `frontend/src/`

UI entry + composition. No data fetching here.

## Files
- `main.jsx:1` — `createRoot` → `<App/>`.
- `App.jsx:1` — layout only (`TaskForm`, `StepList`, `EvidenceCard` via `hooks/useRun.js`). Max ~60 lines.

## Subdirs
- `api/` — fetch/SSE wrappers only.
- `hooks/` — React state only.
- `components/` — presentational only (props in, no direct fetch).
