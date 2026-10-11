import { useState } from "react";

export default function TaskForm({ onSubmit }) {
  const [task, setTask] = useState("");
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(task); }}>
      <textarea value={task} onChange={(e) => setTask(e.target.value)}
        rows={3} style={{ width: "100%" }} placeholder="e.g. Find latest Acme invoice..." />
      <button type="submit">Run</button>
    </form>
  );
}
