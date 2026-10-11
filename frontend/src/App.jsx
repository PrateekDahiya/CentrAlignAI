import TaskForm from "./components/TaskForm.jsx";
import StepList from "./components/StepList.jsx";
import EvidenceCard from "./components/EvidenceCard.jsx";
import ApprovalModal from "./components/ApprovalModal.jsx";
import StatusBadge from "./components/StatusBadge.jsx";
import { useRun } from "./hooks/useRun.js";
import { useApproval } from "./hooks/useApproval.js";

export default function App() {
  const { runId, createRun } = useRun();
  const { status, question, waiting, approve, decline } = useApproval(runId);
  return (
    <main className="app">
      <div className="app-head">
        <h2>Autonomous Task Worker</h2>
        <p>Describe the goal — the agent plans, acts, verifies, and reports back.</p>
      </div>
      <TaskForm onSubmit={createRun} />
      {runId && (
        <p className="run-line">
          run: {runId} <StatusBadge status={status || "running"} />
        </p>
      )}
      {waiting && (
        <ApprovalModal question={question} onApprove={approve} onDecline={decline} />
      )}
      <StepList runId={runId} />
      <EvidenceCard runId={runId} status={status} />
    </main>
  );
}
