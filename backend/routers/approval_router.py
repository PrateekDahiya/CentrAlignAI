"""Approval router: human gate (thin)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.run import Run
from backend.models.fact import Fact
from backend.schemas.approval_schema import ApprovalIn

router = APIRouter(prefix="/api/runs", tags=["approval"])


@router.post("/{run_id}/approve")
def approve(run_id: str, body: ApprovalIn, db: Session = Depends(get_db)):
    run = db.query(Run).filter_by(id=run_id).one()
    db.add(Fact(run_id=run_id, k="user_approval",
                v=f"approved={body.approved} answer={body.answer}"))
    run.status = "running" if body.approved else "cancelled"
    db.commit()
    return {"status": run.status}
