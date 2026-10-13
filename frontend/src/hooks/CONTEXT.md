# CONTEXT.md — `frontend/src/hooks/`

State layer only. No JSX.

## Files
- `useRun.js:1` — `{runId, createRun, clearRun}` via `api/runsApi.js` (`clearRun` resets for New chat).
- `useSidebarWidth.js:1` — `{width, dragging, start}` drag-resize state (220–520px, localStorage persisted).
- `useRunEvents.js:1` — `{events[]}` of raw step JSON strings via `api/sseClient.js`, resubscribes on `runId` change. Dedupes by step `n` in a ref (StrictMode/reconnect safe); closes stream on `done`.
- `useRunHistory.js:1` — `{runs[]}` via `fetchRuns`, refetches on `refreshKey`; polls every 5s only while a run is `running`/`waiting`, stops when all terminal. Logs `useRunEvents` on (re)subscribe.
- `useApproval.js:1` — `useApproval(runId)` → `{status, question, waiting, approve, decline, verified, evidence}`. Polls `fetchStatus` every 2s, stops at `done`/`failed`/`cancelled`. Approve POSTs `{approved:true, answer}` (server resumes); decline POSTs approved false.
