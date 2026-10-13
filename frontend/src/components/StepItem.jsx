const TOOL_TONE = {
  file_list: "tone-file",
  file_read: "tone-file",
  pdf_text: "tone-doc",
  image_text: "tone-doc",
  invoice_parse: "tone-erp",
  erp_list: "tone-erp",
  erp_create: "tone-erp",
  web_search: "tone-web",
  browser_open: "tone-web",
  ask_user: "tone-ask",
};

function toneFor(tool) {
  return TOOL_TONE[tool] || "";
}

function Output({ obs, important }) {
  return (
    <details className="step-details" defaultOpen={important}>
      <summary className="step-summary">
        {important ? "Output — needs attention" : `Output · ${obs.length} chars`}
      </summary>
      <pre className="step-obs">{obs}</pre>
    </details>
  );
}

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
              {p.tool ? <span className={`tool-chip ${toneFor(p.tool)}`}>{p.tool}</span> : null}
            </li>
          ))}
        </ol>
      </div>
    );
  }

  if (event.type === "done" || event.type === "paused") {
    const finished = event.type === "done";
    const final = event.final ? String(event.final).replace(/^FINAL:\s*/, "") : "";
    const question = !finished && event.final
      ? String(event.final).replace(/^ask_user -> paused as waiting:\s*/, "")
      : "";
    return (
      <div className={`step step-${event.type}`}>
        <div className="step-head">
          <span className="step-kind">{finished ? "Answer" : "Paused — input needed"}</span>
          {event.status && <span className="tool-chip">{event.status}</span>}
        </div>
        {finished && final ? <p className="step-final">{final}</p> : null}
        {!finished && question ? <p className="step-question">{question}</p> : null}
        {event.evidence ? <pre className="step-obs">{event.evidence}</pre> : null}
      </div>
    );
  }

  if (event.type === "step") {
    const { n, thought, tool, obs } = event;
    const important =
      tool === "ask_user" || /(paused|failed|refused|not found|error)/i.test(obs || "");
    return (
      <div className="step step-step">
        <div className="step-head">
          <span className="step-num">{n}</span>
          {tool && <span className={`tool-chip ${toneFor(tool)}`}>{tool}</span>}
        </div>
        {thought && <p className="step-thought">{thought}</p>}
        {obs ? <Output obs={obs} important={important} /> : null}
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
