"""Runs router: create run + launch agent in background (thin)."""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.db.engine import SessionLocal
from backend.db.session import get_db
from backend.models.run import Run
from backend.schemas.run_schema import RunCreate, RunOut, RunListOut
from backend.utils.ids import new_run_id
from backend.utils.logging import inside
from backend.agent.loop import run_task

router = APIRouter(prefix="/api/runs", tags=["runs"])


def _execute(run_id: str, task: str) -> None:
    inside("_execute", run_id)
    db = SessionLocal()
    try:
        run_task(db, task, run_id=run_id)
    finally:
        db.close()


@router.post("", response_model=RunOut)
def create_run(body: RunCreate, background: BackgroundTasks,
               db: Session = Depends(get_db)):
    inside("create_run", body.task)
    row = Run(id=new_run_id(), task=body.task, status="running")
    db.add(row)
    db.commit()
    background.add_task(_execute, row.id, body.task)
    return RunOut(id=row.id, task=row.task, status=row.status)


@router.get("", response_model=list[RunListOut])
def list_runs(db: Session = Depends(get_db)):
    inside("list_runs", "-")
    rows = db.query(Run).order_by(Run.created_at.desc()).limit(50).all()
    return [RunListOut(id=r.id, task=r.task, status=r.status,
                       created_at=r.created_at) for r in rows]


@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)):
    inside("get_run", run_id)
    row = db.query(Run).filter_by(id=run_id).one()
    return RunOut(id=row.id, task=row.task, status=row.status)
