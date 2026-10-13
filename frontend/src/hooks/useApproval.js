import { useEffect, useState } from "react";
import { fetchStatus, approveRun } from "../api/runsApi.js";

const TERMINAL = ["done", "failed", "cancelled"];

export function useApproval(runId) {
  const [status, setStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [verified, setVerified] = useState(false);
  const [evidence, setEvidence] = useState("");

  useEffect(() => {
    console.info(`inside useApprovalPoll for ${runId}`);
    if (!runId) return;
    let stop = false;
    let t = null;
    function apply(s) {
      setStatus(s.status);
      setQuestion(s.question || "");
      setVerified(!!s.verified);
      setEvidence(s.evidence || "");
    }
    async function poll() {
      let s;
      try {
        s = await fetchStatus(runId);
      } catch {
        return;
      }
      if (stop) return;
      apply(s);
      if (TERMINAL.includes(s.status) && t) {
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
    await approveRun(runId, true, answer);
    const s = await fetchStatus(runId);
    setStatus(s.status);
  }

  async function decline() {
    console.info(`inside decline for ${runId}`);
    await approveRun(runId, false, "");
    setStatus("cancelled");
  }

  return { status, question, waiting: status === "waiting", approve, decline, verified, evidence };
}
