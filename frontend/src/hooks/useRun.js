import { useState } from "react";
import { createRun as apiCreate } from "../api/runsApi.js";

export function useRun() {
  const [runId, setRunId] = useState(null);
  async function createRun(task) {
    const out = await apiCreate(task);
    setRunId(out.id);
  }
  return { runId, createRun };
}
