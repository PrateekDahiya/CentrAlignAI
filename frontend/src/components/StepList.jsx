import StepItem from "./StepItem.jsx";
import { useRunEvents } from "../hooks/useRunEvents.js";

export default function StepList({ runId }) {
  const events = useRunEvents(runId);
  if (!runId) return null;
  return <div>{events.map((e, i) => <StepItem key={i} text={e} />)}</div>;
}
