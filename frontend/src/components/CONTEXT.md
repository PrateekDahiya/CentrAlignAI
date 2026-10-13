# CONTEXT.md — `frontend/src/components/`

Presentational only. Props in, no direct `fetch`/`EventSource`.

## Files
- `TaskForm.jsx:1` — textarea + Run button (`busy` disables, shows Working…), 3 clickable example chips, clears after submit, `onSubmit(task)` prop.
- `StepList.jsx:1` — subscribes via `useRunEvents(runId)`, empty-state line when idle, renders `StepItem` per event, auto-scrolls to latest, "Agent is working…" footer while `busy`.
- `StepItem.jsx:1` — typed cards: goal (objective + criteria), plan (numbered + tone tool chips), step (number badge + thought + collapsible output, auto-open on errors/questions), done (Answer card, pre-wrapped final) / paused (question callout), fallback note.
- `ApprovalModal.jsx:1` — fixed overlay: question + answer textarea + Approve & resume / Decline. Shown by `App.jsx` when `useApproval(runId).waiting`.
- `EvidenceCard.jsx:1` — run `status` + Verified/Not-verified badge + evidence note + trace download link.
- `StatusBadge.jsx:1` — `running`/`waiting`/`done`/`failed` label.
- `RunHistory.jsx:1` — searchable past-run list (status dot + live pulse, relative time, 2-line clamp) via `useRunHistory`; `onSelect(id)` switches the displayed run (steps reload from SSE replay, approval follows).
