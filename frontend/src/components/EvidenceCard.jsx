import StatusBadge from "./StatusBadge.jsx";
import { API_BASE } from "../api/base.js";

export default function EvidenceCard({ runId, status, verified, evidence }) {
  if (!runId) return null;
  const terminal = status === "done" || status === "failed";
  return (
    <div className="evidence">
      <div>
        <StatusBadge status={status || "running"} />
        {terminal && (
          <span className={verified ? "verdict-ok" : "verdict-bad"}>
            {verified ? "Verified" : "Not verified"}
          </span>
        )}
        {evidence ? <p className="evidence-note">{evidence}</p> : null}
      </div>
      <a
        className="btn btn-ghost btn-sm"
        href={`${API_BASE}/api/runs/${runId}/trace`}
        target="_blank"
        rel="noreferrer"
      >
        Download trace
      </a>
    </div>
  );
}
