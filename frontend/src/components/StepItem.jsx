export default function StepItem({ event }) {
  if (!event) return null;

  if (event.type === "goal" && event.goal) {
    const g = event.goal;
    return (
      <div className="step step-goal">
        <div className="step-head"><span className="step-kind">Goal</span></div>
        <p className="step-final">{g.objective}</p>
        {(g.success_criteria || []).length > 0 && (
          <ul className="step-list">
            {g.success_criteria.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        )}
      </div>
    );
  }

  if (event.type === "plan" && Array.isArray(event.plan)) {
    return (
      <div className="step step-plan">
        <div className="step-head">
          <span className="step-kind">Plan · {event.plan.length} steps</span>
        </div>
        <ol className="step-list">
          {event.plan.map((p, i) => (
            <li key={i}>
              {p.step}{" "}
              {p.tool ? <span className="tool-chip">{p.tool}</span> : null}
            </li>
          ))}
        </ol>
      </div>
    );
  }

  if (event.type === "done" || event.type === "paused") {
    const finished = event.type === "done";
    return (
      <div className={`step step-${event.type}`}>
        <div className="step-head">
          <span className="step-kind">{finished ? "Finished" : "Paused"}</span>
          {event.status && <span className="tool-chip">{event.status}</span>}
        </div>
        {event.final ? (
          <p className="step-final">
            {String(event.final).replace(/^FINAL:\s*/, "")}
          </p>
        ) : null}
        {event.evidence ? <pre className="step-obs">{event.evidence}</pre> : null}
      </div>
    );
  }

  if (event.type === "step") {
    const { n, thought, tool, obs } = event;
    return (
      <div className="step step-step">
        <div className="step-head">
          <span className="step-kind">Step {n}</span>
          {tool && <span className="tool-chip">{tool}</span>}
        </div>
        {thought && <p className="step-thought">{thought}</p>}
        {obs && <pre className="step-obs">{obs}</pre>}
      </div>
    );
  }

  return (
    <div className="step step-note">
      <span className="step-kind">{event.type || "message"}</span>
      {event.text ? <p className="step-thought">{event.text}</p> : null}
    </div>
  );
}
