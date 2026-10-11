export default function StepItem({ step }) {
  if (!step) return null;
  const { n, thought, tool, obs } = step;
  const cls = n % 2 === 0 ? "step-even" : "step-odd";
  return (
    <div className={`step ${cls}`}>
      <div className="step-head">
        <span className="step-kind">Step {n}</span>
        {tool && <span className="tool-chip">{tool}</span>}
      </div>
      {thought && <p className="step-thought">{thought}</p>}
      {obs && (
        <pre className="step-obs">{obs}</pre>
      )}
    </div>
  );
}