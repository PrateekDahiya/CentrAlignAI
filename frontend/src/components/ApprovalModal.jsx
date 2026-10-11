import { useState } from "react";

export default function ApprovalModal({ question, onApprove, onDecline }) {
  const [answer, setAnswer] = useState("");
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)" }}>
      <div style={{ background: "#fff", margin: "15% auto", padding: 16, maxWidth: 480 }}>
        <h3>Agent needs your input</h3>
        <p>{question}</p>
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          rows={2}
          style={{ width: "100%" }}
          placeholder="Type your answer..."
        />
        <button onClick={() => onApprove(answer)}>Approve & resume</button>
        <button onClick={onDecline}>Decline</button>
      </div>
    </div>
  );
}
