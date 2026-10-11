"""Run status + latest question (thin, for UI polling)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.run import Run
from backend.models.fact import Fact
from backend.utils.logging import inside

router = APIRouter(prefix="/api/runs", tags=["status"])


@router.get("/{run_id}/status")
def get_status(run_id: str, db: Session = Depends(get_db)):
    inside("get_status", run_id)
    run = db.query(Run).filter_by(id=run_id).one()
    q = db.query(Fact).filter_by(run_id=run_id, k="question").order_by(Fact.id.desc()).first()
    return {"status": run.status, "question": q.v if q else ""}
