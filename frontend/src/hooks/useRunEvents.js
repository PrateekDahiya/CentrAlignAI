import { useEffect, useState } from "react";
import { subscribeEvents } from "../api/sseClient.js";

export function useRunEvents(runId) {
  const [events, setEvents] = useState([]);
  useEffect(() => subscribeEvents(runId, (m) => setEvents((p) => [...p, m])), [runId]);
  return events;
}
