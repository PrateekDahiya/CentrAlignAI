import { useEffect, useState } from "react";
import { fetchRuns } from "../api/runsApi.js";

export function useRunHistory(refreshKey) {
  const [runs, setRuns] = useState([]);

  useEffect(() => {
    console.info(`inside useRunHistory for ${refreshKey}`);
    let stop = false;
    async function load() {
      try {
        const list = await fetchRuns();
        if (!stop) setRuns(list);
      } catch {
        /* server may restart; retry next poll */
      }
    }
    load();
    const t = setInterval(load, 5000);
    return () => {
      stop = true;
      clearInterval(t);
    };
  }, [refreshKey]);

  return { runs };
}
