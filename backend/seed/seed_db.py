"""Create MySQL tables only."""
from backend.db.base import Base
from backend.db.engine import engine
import backend.models.run  # noqa: F401
import backend.models.step  # noqa: F401
import backend.models.fact  # noqa: F401
import backend.models.invoice  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("tables created")


if __name__ == "__main__":
    init_db()
