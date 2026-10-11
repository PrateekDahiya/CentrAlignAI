export default function EvidenceCard({ runId }) {
  if (!runId) return null;
  return <a href={`/api/runs/${runId}/trace`} target="_blank" rel="noreferrer">Download trace</a>;
}
