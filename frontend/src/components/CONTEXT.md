# CONTEXT.md — `frontend/src/components/`

Presentational only. Props in, no direct `fetch`/`EventSource`.

## Files
- `TaskForm.jsx:1` — textarea + Run button, `onSubmit(task)` prop.
- `StepList.jsx:1` — subscribes via `useRunEvents(runId)`, renders `StepItem` list.
- `StepItem.jsx:1` — single `<pre>` thought/tool/obs row.
- `ApprovalModal.jsx:1` — placeholder (Phase 4: waiting gate using `useApproval`).
- `EvidenceCard.jsx:1` — trace download link `/api/runs/{id}/trace` (Phase 4: + ERP row, PDF link, verified badge).
- `StatusBadge.jsx:1` — `running`/`waiting`/`done`/`failed` label.
