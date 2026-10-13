# CONTEXT.md — `frontend/src/components/`

Presentational only. Props in, no direct `fetch`/`EventSource`.

## Files
- `TaskForm.jsx:1` — textarea + Run button (`busy` disables, shows Working…), 3 clickable example chips, `onSubmit(task)` prop.
- `StepList.jsx:1` — subscribes via `useRunEvents(runId)`, empty-state line when idle, renders `StepItem` per event.
- `StepItem.jsx:1` — typed cards: goal (objective + criteria), plan (numbered + tool chips), step (thought + scrollable obs), done/paused (final + evidence), fallback note.
- `ApprovalModal.jsx:1` — fixed overlay: question + answer textarea + Approve & resume / Decline. Shown by `App.jsx` when `useApproval(runId).waiting`.
- `EvidenceCard.jsx:1` — run `status` + Verified/Not-verified badge + evidence note + trace download link.
- `StatusBadge.jsx:1` — `running`/`waiting`/`done`/`failed` label.
- `RunHistory.jsx:1` — clickable past-run list (task + timestamp + badge) via `useRunHistory`; `onSelect(id)` switches the displayed run (steps reload from SSE replay, approval follows).
