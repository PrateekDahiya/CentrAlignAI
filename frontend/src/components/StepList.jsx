import { useEffect, useRef } from "react";
import StepItem from "./StepItem.jsx";
import { useRunEvents } from "../hooks/useRunEvents.js";

function parse(e) {
  try {
    return JSON.parse(e);
  } catch {
    return { type: "message", text: e };
  }
}

export default function StepList({ runId, busy }) {
  const events = useRunEvents(runId);
  const endRef = useRef(null);
  useEffect(() => {
    // Follow the stream only if the user is already near the bottom —
    // never yank the viewport away from what they're reading.
    const nearBottom =
      window.innerHeight + window.scrollY >=
      document.documentElement.scrollHeight - 160;
    if (nearBottom) {
      endRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }, [events.length, runId]);
  if (!runId) return null;
  if (!events.length) {
    return <p className="empty">Waiting for the agent’s first step…</p>;
  }
  return (
    <div className="steps">
      {events.map((e, i) => {
        const ev = parse(e);
        return <StepItem key={ev.n ?? i} event={ev} />;
      })}
      <div ref={endRef} />
      {busy && (
        <p className="working">
          <span className="dot dot-running pulse" /> Agent is working…
        </p>
      )}
    </div>
  );
}
