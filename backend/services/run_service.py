"""Run service: DB ops only, no LLM."""
from sqlalchemy.orm import Session
from backend.models.run import Run
from backend.utils.ids import new_run_id


def create_run(db: Session, task: str) -> Run:
    row = Run(id=new_run_id(), task=task, status="running")
    db.add(row)
    db.commit()
    return row


def set_status(db: Session, run_id: str, status: str) -> None:
    db.query(Run).filter_by(id=run_id).update({"status": status})
    db.commit()
