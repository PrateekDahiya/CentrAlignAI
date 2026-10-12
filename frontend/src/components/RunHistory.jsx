import { useRunHistory } from "../hooks/useRunHistory.js";
import StatusBadge from "./StatusBadge.jsx";

export default function RunHistory({ selectedId, liveId, onSelect, refreshKey }) {
  const { runs } = useRunHistory(refreshKey);
  if (!runs.length) return null;
  const shown = selectedId || liveId;
  return (
    <div className="history">
      <h3>History</h3>
      {runs.map((r) => (
        <button
          key={r.id}
          className={`history-item${r.id === shown ? " selected" : ""}`}
          onClick={() => onSelect(r.id)}
        >
          <span className="history-task">{r.task}</span>
          <StatusBadge status={r.status} />
        </button>
      ))}
    </div>
  );
}
