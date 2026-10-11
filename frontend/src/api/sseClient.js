export function subscribeEvents(runId, onMsg) {
  console.info(`inside subscribeEvents for ${runId}`);
  if (!runId) return () => {};
  const es = new EventSource(`/api/runs/${runId}/events`);
  
  // Only handle 'step' events
  es.addEventListener('step', (e) => {
    console.info(`received step event: ${e.data}`);
    onMsg(e.data);
  });
  
  // Optional: log other event types for debugging
  es.addEventListener('goal', (e) => {
    console.info(`received goal event (not rendering)`);
  });
  es.addEventListener('plan', (e) => {
    console.info(`received plan event (not rendering)`);
  });
  es.addEventListener('done', (e) => {
    console.info(`received done event`);
  });
  
  return () => es.close();
}
