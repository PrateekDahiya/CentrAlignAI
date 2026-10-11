import { useState } from "react";

export default function ApprovalModal({ question, onApprove, onDecline }) {
  const [answer, setAnswer] = useState("");
  return (
    <div className="modal-veil">
      <div className="modal">
        <h3>Agent needs your input</h3>
        <p className="q">{question}</p>
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          rows={2}
          placeholder="Type your answer..."
        />
        <div className="modal-actions">
          <button className="btn" onClick={() => onApprove(answer)}>
            Approve & resume
          </button>
          <button className="btn btn-ghost" onClick={onDecline}>
            Decline
          </button>
        </div>
      </div>
    </div>
  );
}
