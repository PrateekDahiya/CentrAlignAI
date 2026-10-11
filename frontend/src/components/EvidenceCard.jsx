export default function EvidenceCard({ runId, status }) {
  if (!runId) return null;
  return (
    <div>
      <p>status: {status || "running"}</p>
      <a href={`/api/runs/${runId}/trace`} target="_blank" rel="noreferrer">
        Download trace
      </a>
    </div>
  );
}
