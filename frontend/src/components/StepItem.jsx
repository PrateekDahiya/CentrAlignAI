export default function StepItem({ text }) {
  let ev;
  try {
    ev = JSON.parse(text);
  } catch {
    return <pre className="step raw">{text}</pre>;
  }
  const kind = ev.type || "message";
  const step = ev.step || {};
  return (
    <div className={`step step-${kind}`}>
      <div className="step-head">
        <span className="step-kind">
          {kind}
          {ev.n ? ` #${ev.n}` : ""}
        </span>
        {step.tool && <span className="tool-chip">{step.tool}</span>}
      </div>
      {ev.goal && (
        <>
          <p className="step-final">{ev.goal.objective}</p>
          <ul className="step-list">
            {(ev.goal.success_criteria || []).map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </>
      )}
      {ev.plan && (
        <ol className="step-list">
          {ev.plan.map((p, i) => (
            <li key={i}>
              {p.step} {p.tool ? <span className="tool-chip">{p.tool}</span> : null}
            </li>
          ))}
        </ol>
      )}
      {step.thought && <p className="step-thought">{step.thought}</p>}
      {step.obs && <pre className="step-obs">{step.obs}</pre>}
      {(kind === "done" || kind === "paused") && ev.final && (
        <p className="step-final">{ev.final}</p>
      )}
    </div>
  );
}
