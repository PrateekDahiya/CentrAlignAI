import { useEffect, useState } from "react";
import { subscribeEvents } from "../api/sseClient.js";

export function useRunEvents(runId) {
  const [events, setEvents] = useState([]);
  const [isDone, setIsDone] = useState(false);
  
  useEffect(() => {
    console.info(`inside useRunEvents for ${runId}`);
    // Reset events when runId changes (new run)
    setEvents([]);
    setIsDone(false);
    
    if (!runId) return;
    
    const cleanup = subscribeEvents(runId, (m) => {
      try {
        const ev = JSON.parse(m);
        // Only add step events
        if (ev.type === "step") {
          setEvents((p) => [...p, m]);
        }
        // Stop collecting after done
        if (ev.type === "done") {
          setIsDone(true);
        }
      } catch (e) {
        console.error("Error parsing event:", e);
      }
    });
    
    return cleanup;
  }, [runId]);
  
  return events;
}
