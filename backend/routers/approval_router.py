"""Approval router: human gate + resume agent in background (thin)."""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.db.engine import SessionLocal
from backend.db.session import get_db
from backend.models.run import Run
from backend.models.fact import Fact
from backend.schemas.approval_schema import ApprovalIn
from backend.utils.logging import inside
from backend.agent.loop import resume_task

router = APIRouter(prefix="/api/runs", tags=["approval"])


def _resume(run_id: str) -> None:
    inside("approve_resume", run_id)
    db = SessionLocal()
    try:
        resume_task(db, run_id)
    finally:
        db.close()


@router.post("/{run_id}/approve")
def approve(run_id: str, body: ApprovalIn, background: BackgroundTasks,
            db: Session = Depends(get_db)):
    inside("approve", run_id)
    run = db.query(Run).filter_by(id=run_id).one()
    db.add(Fact(run_id=run_id, k="user_approval",
                v=f"approved={body.approved} answer={body.answer}"))
    run.status = "running" if body.approved else "cancelled"
    db.commit()
    if body.approved:
        background.add_task(_resume, run_id)
    return {"status": run.status}
