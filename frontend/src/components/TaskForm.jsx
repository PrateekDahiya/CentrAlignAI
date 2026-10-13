import { useState } from "react";

const EXAMPLES = [
  {
    label: "Invoice → ERP",
    task: "Enter invoice file Acme_Corp_INV-1002.pdf from the inbox into the ERP: parse it and create the ERP row, then confirm done.",
  },
  {
    label: "Latest invoice (asks)",
    task: "Find the latest invoice from Acme Corp, extract the amount and due date, enter it into our internal system, and tell me once it is done.",
  },
  {
    label: "Web price lookup",
    task: "Search the web for the price of Logitech MX Master 3S and log the result into the ERP system.",
  },
];

export default function TaskForm({ onSubmit, busy }) {
  const [task, setTask] = useState("");

  function submit(value) {
    const v = (value ?? task).trim();
    if (!v || busy) return;
    console.info(`inside TaskFormSubmit for ${v}`);
    onSubmit(v);
  }

  return (
    <form
      className="task-form"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
    >
      <textarea
        value={task}
        onChange={(e) => setTask(e.target.value)}
        rows={3}
        placeholder="e.g. Find latest Acme invoice, enter it into ERP, tell me when done"
      />
      <div className="task-actions">
        <button className="btn" type="submit" disabled={busy}>
          {busy ? "Working…" : "Run agent"}
        </button>
      </div>
      <div className="examples">
        <span className="examples-label">Try:</span>
        {EXAMPLES.map((ex) => (
          <button
            key={ex.label}
            type="button"
            className="chip"
            disabled={busy}
            onClick={() => {
              setTask(ex.task);
              submit(ex.task);
            }}
          >
            {ex.label}
          </button>
        ))}
      </div>
    </form>
  );
}
