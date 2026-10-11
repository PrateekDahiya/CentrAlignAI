# CONTEXT.md — `frontend/src/hooks/`

State layer only. No JSX.

## Files
- `useRun.js:1` — `{runId, createRun}` via `api/runsApi.js`.
- `useRunEvents.js:1` — `{events[]}` subscribed via `api/sseClient.js`, resubscribes on `runId` change. Logs `useRunEvents` on (re)subscribe.
- `useApproval.js:1` — `useApproval(runId)` → `{status, question, waiting, approve, decline}`. Polls `fetchStatus` every 2s, stops at `done`/`cancelled`. Approve POSTs `{approved:true, answer}` (server resumes); decline POSTs approved false.
