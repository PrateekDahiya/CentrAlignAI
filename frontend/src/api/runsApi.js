import { API_BASE } from "./base.js";

export async function createRun(task) {
  console.info(`inside createRun for ${task}`);
  const r = await fetch(`${API_BASE}/api/runs`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task })
  });
  return r.json();
}

export async function fetchTrace(runId) {
  console.info(`inside fetchTrace for ${runId}`);
  const r = await fetch(`${API_BASE}/api/runs/${runId}/trace`);
  return r.json().catch(() => r.text());
}

export async function fetchStatus(runId) {
  console.info(`inside fetchStatus for ${runId}`);
  const r = await fetch(`${API_BASE}/api/runs/${runId}/status`);
  return r.json();
}

export async function fetchRuns() {
  console.info(`inside fetchRuns for -`);
  const r = await fetch(`${API_BASE}/api/runs`);
  return r.json();
}
