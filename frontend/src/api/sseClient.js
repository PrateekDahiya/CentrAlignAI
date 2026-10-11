export function subscribeEvents(runId, onMsg) {
  console.info(`inside subscribeEvents for ${runId}`);
  if (!runId) return () => {};
  const es = new EventSource(`/api/runs/${runId}/events`);
  es.onmessage = (e) => onMsg(e.data);
  return () => es.close();
}
