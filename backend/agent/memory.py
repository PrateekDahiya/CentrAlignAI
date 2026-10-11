"""Agent memory: facts table CRUD. No LLM."""
from sqlalchemy.orm import Session
from backend.models.fact import Fact


def save_fact(db: Session, run_id: str, k: str, v: str) -> None:
    db.add(Fact(run_id=run_id, k=k, v=str(v)))
    db.commit()


def get_facts(db: Session, run_id: str) -> dict:
    return {r.k: r.v for r in db.query(Fact).filter_by(run_id=run_id).all()}
