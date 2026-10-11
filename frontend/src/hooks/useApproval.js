import { useState } from "react";

export function useApproval() {
  const [waiting, setWaiting] = useState(false);
  async function approve(runId, approved, answer) {
    console.info(`inside approve for ${runId}`);
    await fetch(`/api/runs/${runId}/approve`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ approved, answer })
    });
    setWaiting(false);
  }
  return { waiting, setWaiting, approve };
}
