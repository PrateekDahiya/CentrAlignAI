# CONTEXT.md — `frontend/src/api/`

Network layer only. No JSX, no state.

## Files
- `runsApi.js:1` — `createRun(task)` POST `/api/runs`, `fetchTrace(runId)` GET `/api/runs/{id}/trace`.
- `sseClient.js:1` — `subscribeEvents(runId,onMsg)` → `EventSource(/api/runs/{id}/events)`, returns unsubscribe.
