export default function StatusBadge({ status }) {
  const s = (status || "unknown").toLowerCase();
  return <span className={`badge badge-${s}`}>{status}</span>;
}
