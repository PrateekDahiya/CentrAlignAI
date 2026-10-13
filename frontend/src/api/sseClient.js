const FORWARD = ["step", "goal", "plan", "paused", "resumed", "timeout"];

import { API_BASE } from "./base.js";

export function subscribeEvents(runId, onMsg, onDone) {
  console.info(`inside subscribeEvents for ${runId}`);
  if (!runId) return () => {};
  const es = new EventSource(`${API_BASE}/api/runs/${runId}/events`);
  const close = () => es.close();

  FORWARD.forEach((t) =>
    es.addEventListener(t, (e) => {
      onMsg(e.data);
    })
  );

  // 'done' closes the stream: otherwise EventSource auto-reconnects and the
  // server replays the whole trace, appending every step a second time.
  es.addEventListener("done", (e) => {
    console.info(`received done event, closing stream`);
    onMsg(e.data);
    if (onDone) onDone();
    close();
  });

  return close;
}
