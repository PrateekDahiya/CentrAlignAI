import { useEffect, useState } from "react";
import { fetchRuns } from "../api/runsApi.js";

export function useRunHistory(refreshKey) {
  const [runs, setRuns] = useState([]);

  useEffect(() => {
    console.info(`inside useRunHistory for ${refreshKey}`);
    let stop = false;
    let t = null;
    async function load() {
      let list;
      try {
        list = await fetchRuns();
      } catch {
        return; /* server may restart; retry next poll */
      }
      if (stop) return;
      setRuns(list);
      // No active agent -> stop polling until a new run appears.
      const active = list.some(
        (r) => r.status === "running" || r.status === "waiting"
      );
      if (!active && t) {
        clearInterval(t);
        t = null;
      }
    }
    load();
    t = setInterval(load, 5000);
    return () => {
      stop = true;
      if (t) clearInterval(t);
    };
  }, [refreshKey]);

  return { runs };
}
