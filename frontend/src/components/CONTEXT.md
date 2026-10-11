# CONTEXT.md — `frontend/src/components/`

Presentational only. Props in, no direct `fetch`/`EventSource`.

## Files
- `TaskForm.jsx:1` — textarea + Run button, `onSubmit(task)` prop.
- `StepList.jsx:1` — subscribes via `useRunEvents(runId)`, renders `StepItem` list.
- `StepItem.jsx:1` — single `<pre>` thought/tool/obs row.
- `ApprovalModal.jsx:1` — fixed overlay: question + answer textarea + Approve & resume / Decline. Shown by `App.jsx` when `useApproval(runId).waiting`.
- `EvidenceCard.jsx:1` — run `status` + trace download link (verified badge + ERP row in Phase 5).
- `StatusBadge.jsx:1` — `running`/`waiting`/`done`/`failed` label.
