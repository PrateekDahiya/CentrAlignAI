import { useRunHistory } from "../hooks/useRunHistory.js";
import StatusBadge from "./StatusBadge.jsx";

function fmtTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return isNaN(d) ? "" : d.toLocaleString();
}

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
          <span className="history-main">
            <span className="history-task">{r.task}</span>
            <span className="history-time">{fmtTime(r.created_at)}</span>
          </span>
          <StatusBadge status={r.status} />
        </button>
      ))}
    </div>
  );
}
