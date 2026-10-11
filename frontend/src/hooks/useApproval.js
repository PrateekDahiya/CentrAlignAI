import { useEffect, useState } from "react";
import { fetchStatus } from "../api/runsApi.js";

export function useApproval(runId) {
  const [status, setStatus] = useState("");
  const [question, setQuestion] = useState("");

  useEffect(() => {
    console.info(`inside useApprovalPoll for ${runId}`);
    if (!runId) return;
    let stop = false;
    let t = null;
    async function poll() {
      let s;
      try {
        s = await fetchStatus(runId);
      } catch {
        return;
      }
      if (stop) return;
      setStatus(s.status);
      setQuestion(s.question || "");
      if ((s.status === "done" || s.status === "cancelled") && t) {
        clearInterval(t);
        t = null;
      }
    }
    poll();
    t = setInterval(poll, 2000);
    return () => {
      stop = true;
      if (t) clearInterval(t);
    };
  }, [runId]);

  async function approve(answer) {
    console.info(`inside approve for ${runId}`);
    await fetch(`/api/runs/${runId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ approved: true, answer })
    });
    const s = await fetchStatus(runId);
    setStatus(s.status);
  }

  async function decline() {
    console.info(`inside decline for ${runId}`);
    await fetch(`/api/runs/${runId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ approved: false, answer: "" })
    });
    setStatus("cancelled");
  }

  return { status, question, waiting: status === "waiting", approve, decline };
}
