import { useState } from "react";
import { useRunHistory } from "../hooks/useRunHistory.js";

const DOT = {
  running: "dot-running",
  waiting: "dot-waiting",
  done: "dot-done",
  failed: "dot-failed",
  cancelled: "dot-cancelled",
};

function fmtRel(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  const s = (Date.now() - d.getTime()) / 1000;
  if (s < 60) return "just now";
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return d.toLocaleDateString();
}

export default function RunHistory({ selectedId, liveId, onSelect, refreshKey }) {
  const { runs } = useRunHistory(refreshKey);
  const [q, setQ] = useState("");
  const shown = selectedId || liveId;
  const needle = q.trim().toLowerCase();
  const filtered = needle
    ? runs.filter((r) => (r.task || "").toLowerCase().includes(needle))
    : runs;
  return (
    <div className="history">
      <div className="history-head">
        <h3>Runs</h3>
        <span className="history-count">{runs.length}</span>
      </div>
      <input
        className="history-search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search runs…"
      />
      {!runs.length && (
        <p className="history-empty">No runs yet — describe a goal to start.</p>
      )}
      {filtered.map((r) => {
        const live =
          r.id === liveId && (r.status === "running" || r.status === "waiting");
        return (
          <button
            key={r.id}
            title={r.task}
            className={`history-item${r.id === shown ? " selected" : ""}`}
            onClick={() => onSelect(r.id)}
          >
            <span className={`dot ${DOT[r.status] || ""}${live ? " pulse" : ""}`} />
            <span className="history-main">
              <span className="history-task clamp">{r.task}</span>
              <span className="history-time">
                {fmtRel(r.created_at)}
                {live ? " · live" : ""}
              </span>
            </span>
          </button>
        );
      })}
      {runs.length > 0 && !filtered.length && (
        <p className="history-empty">No matches.</p>
      )}
    </div>
  );
}
