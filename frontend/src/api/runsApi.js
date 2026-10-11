export async function createRun(task) {
  const r = await fetch("/api/runs", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task })
  });
  return r.json();
}

export async function fetchTrace(runId) {
  const r = await fetch(`/api/runs/${runId}/trace`);
  return r.json().catch(() => r.text());
}
