import TaskForm from "./components/TaskForm.jsx";
import StepList from "./components/StepList.jsx";
import EvidenceCard from "./components/EvidenceCard.jsx";
import { useRun } from "./hooks/useRun.js";

export default function App() {
  const { runId, createRun } = useRun();
  return (
    <main style={{ maxWidth: 720, margin: "24px auto", fontFamily: "sans-serif" }}>
      <h2>Autonomous Task Worker</h2>
      <TaskForm onSubmit={createRun} />
      {runId && <p>run: {runId}</p>}
      <StepList runId={runId} />
      <EvidenceCard runId={runId} />
    </main>
  );
}
