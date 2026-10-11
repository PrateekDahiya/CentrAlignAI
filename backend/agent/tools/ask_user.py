"""Pause loop for human input. Phase 4 adds resume UX."""
from sqlalchemy.orm import Session
from backend.models.run import Run
from backend.models.fact import Fact
from backend.utils.logging import inside


def ask_user(db: Session, run_id: str, question: str = "") -> str:
    inside("ask_user", run_id)
    db.add(Fact(run_id=run_id, k="question", v=question or "(no question)"))
    db.query(Run).filter_by(id=run_id).update({"status": "waiting"})
    db.commit()
    return f"paused as waiting: {question} (approve via POST /api/runs/{run_id}/approve)"


SCHEMAS = [
    {"type": "function", "function": {
        "name": "ask_user",
        "description": "Ask the user for clarification; pauses the run until approved",
        "parameters": {"type": "object", "properties": {
            "question": {"type": "string"}}, "required": ["question"]}}},
]
