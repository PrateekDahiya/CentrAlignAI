import { useEffect, useRef, useState } from "react";
import { subscribeEvents } from "../api/sseClient.js";

const KEEP = ["step", "goal", "plan", "done", "paused", "resumed", "timeout"];

export function useRunEvents(runId) {
  const [events, setEvents] = useState([]);
  // Raw messages already shown. Survives StrictMode remounts and any
  // reconnect replay, so an event is never appended twice.
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
          if (!KEEP.includes(ev.type)) return;
          if (seen.current.has(m)) return;
          seen.current.add(m);
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
