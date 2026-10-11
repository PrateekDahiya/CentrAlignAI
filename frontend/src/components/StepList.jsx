import StepItem from "./StepItem.jsx";
import { useRunEvents } from "../hooks/useRunEvents.js";

export default function StepList({ runId }) {
  const events = useRunEvents(runId);
  if (!runId) return null;
  // events is an array of raw SSE message strings (JSON objects)
  const rendered = events.map((e, i) => {
    try {
      const ev = JSON.parse(e);
      // Extract step from the nested structure
      const step = ev.step ? { ...ev.step, n: ev.n } : ev;
      return <StepItem key={i} step={step} />;
    } catch {
      // fallback: show raw text
      return <StepItem key={i} step={{ text: e }} />;
    }
  });
  return <div className="steps">{rendered}</div>;
}
