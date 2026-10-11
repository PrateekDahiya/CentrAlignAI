# CONTEXT.md — `frontend/src/hooks/`

State layer only. No JSX.

## Files
- `useRun.js:1` — `{runId, createRun}` via `api/runsApi.js`.
- `useRunEvents.js:1` — `{events[]}` subscribed via `api/sseClient.js`, resubscribes on `runId` change.
- `useApproval.js:1` — `{waiting, setWaiting, approve(runId,approved,answer)}` POST `/api/runs/{id}/approve` (modal wiring Phase 4).
