import { useEffect, useRef, useState } from "react";
import { subscribeEvents } from "../api/sseClient.js";

export function useRunEvents(runId) {
  const [events, setEvents] = useState([]);
  // Step numbers already shown. Survives StrictMode remounts and any
  // reconnect replay, so a step is never appended twice.
  const seen = useRef(new Set());

  useEffect(() => {
    console.info(`inside useRunEvents for ${runId}`);
    // Reset events when runId changes (new run)
    setEvents([]);
    seen.current = new Set();

    if (!runId) return;

    const cleanup = subscribeEvents(
      runId,
      (m) => {
        try {
          const ev = JSON.parse(m);
          // Only add step events
          if (ev.type !== "step") return;
          const key = ev.n ?? m;
          if (seen.current.has(key)) return;
          seen.current.add(key);
          setEvents((p) => [...p, m]);
        } catch (e) {
          console.error("Error parsing event:", e);
        }
      },
      () => cleanup()
    );

    return cleanup;
  }, [runId]);

  return events;
}
