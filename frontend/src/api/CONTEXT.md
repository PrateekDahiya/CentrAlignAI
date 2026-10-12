# CONTEXT.md — `frontend/src/api/`

Network layer only. No JSX, no state.

## Files
- `runsApi.js:1` — `createRun(task)` POST `/api/runs`, `fetchTrace(runId)` GET trace, `fetchStatus(runId)` GET `/api/runs/{id}/status`, `fetchRuns()` GET `/api/runs` (history list).
- `sseClient.js:1` — `subscribeEvents(runId,onMsg,onDone)` → `EventSource(/api/runs/{id}/events)`, forwards `step` events, closes on `done` (prevents auto-reconnect replay loop). Returns close fn.
