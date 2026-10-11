"""Runs router: create/get run rows (thin, no LLM here)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.run import Run
from backend.schemas.run_schema import RunCreate, RunOut
from backend.utils.ids import new_run_id

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("", response_model=RunOut)
def create_run(body: RunCreate, db: Session = Depends(get_db)):
    row = Run(id=new_run_id(), task=body.task, status="running")
    db.add(row)
    db.commit()
    return RunOut(id=row.id, task=row.task, status=row.status)


@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)):
    row = db.query(Run).filter_by(id=run_id).one()
    return RunOut(id=row.id, task=row.task, status=row.status)
