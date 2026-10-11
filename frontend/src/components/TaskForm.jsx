import { useState } from "react";

export default function TaskForm({ onSubmit }) {
  const [task, setTask] = useState("");
  return (
    <form
      className="task-form"
      onSubmit={(e) => {
        e.preventDefault();
        console.info(`inside TaskFormSubmit for ${task}`);
        onSubmit(task);
      }}
    >
      <textarea
        value={task}
        onChange={(e) => setTask(e.target.value)}
        rows={3}
        placeholder="e.g. Find latest Acme invoice, enter it into ERP, tell me when done"
      />
      <button className="btn" type="submit">
        Run agent
      </button>
    </form>
  );
}
