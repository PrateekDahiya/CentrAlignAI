"""FastAPI DB dependency only."""
from collections.abc import Generator
from sqlalchemy.orm import Session
from backend.db.engine import SessionLocal
from backend.utils.logging import inside


def get_db() -> Generator[Session, None, None]:
    inside("get_db", "-")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
