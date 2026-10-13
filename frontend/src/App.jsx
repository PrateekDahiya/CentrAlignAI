import { useState } from "react";
import TaskForm from "./components/TaskForm.jsx";
import StepList from "./components/StepList.jsx";
import RunHistory from "./components/RunHistory.jsx";
import EvidenceCard from "./components/EvidenceCard.jsx";
import { useRun } from "./hooks/useRun.js";
import { useApproval } from "./hooks/useApproval.js";
import StatusBadge from "./components/StatusBadge.jsx";
import ApprovalModal from "./components/ApprovalModal.jsx";

export default function App() {
  const { runId, createRun } = useRun();
  const [viewId, setViewId] = useState(null);
  const shownId = viewId || runId;
  const { status, question, waiting, approve, decline, verified, evidence } =
    useApproval(shownId);
  const busy =
    !!shownId && (status === "" || status === "running" || status === "waiting");
  return (
    <div className="layout">
      <aside className="sidebar">
        <RunHistory
          selectedId={viewId}
          liveId={runId}
          onSelect={setViewId}
          refreshKey={runId}
        />
      </aside>
      <main className="app">
        <div className="app-head">
          <h2>Autonomous Task Worker</h2>
          <p>Describe the goal — the agent plans, acts, verifies, and reports back.</p>
        </div>
        <TaskForm
          busy={busy}
          onSubmit={(t) => {
            setViewId(null);
            createRun(t);
          }}
        />
        {shownId && (
          <p className="run-line">
            run: {String(shownId).slice(0, 8)}…{" "}
            <StatusBadge status={status || "running"} />
          </p>
        )}
        {waiting && (
          <ApprovalModal question={question} onApprove={approve} onDecline={decline} />
        )}
        <h3>Steps</h3>
        <StepList runId={shownId} />
        <EvidenceCard
          runId={shownId}
          status={status}
          verified={verified}
          evidence={evidence}
        />
      </main>
    </div>
  );
}
