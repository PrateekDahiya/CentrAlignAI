import StatusBadge from "./StatusBadge.jsx";

export default function EvidenceCard({ runId, status }) {
  if (!runId) return null;
  return (
    <div className="evidence">
      <StatusBadge status={status || "running"} />
      <a href={`/api/runs/${runId}/trace`} target="_blank" rel="noreferrer">
        Download trace
      </a>
    </div>
  );
}
