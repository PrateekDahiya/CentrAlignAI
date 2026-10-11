export function subscribeEvents(runId, onMsg) {
  if (!runId) return () => {};
  const es = new EventSource(`/api/runs/${runId}/events`);
  es.onmessage = (e) => onMsg(e.data);
  return () => es.close();
}
