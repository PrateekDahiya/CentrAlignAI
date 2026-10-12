export function subscribeEvents(runId, onMsg, onDone) {
  console.info(`inside subscribeEvents for ${runId}`);
  if (!runId) return () => {};
  const es = new EventSource(`/api/runs/${runId}/events`);
  const close = () => es.close();

  // Only handle 'step' events
  es.addEventListener('step', (e) => {
    console.info(`received step event: ${e.data}`);
    onMsg(e.data);
  });

  // 'done' closes the stream: otherwise EventSource auto-reconnects and the
  // server replays the whole trace, appending every step a second time.
  es.addEventListener('done', () => {
    console.info(`received done event, closing stream`);
    if (onDone) onDone();
    close();
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
  
  return close;
}
