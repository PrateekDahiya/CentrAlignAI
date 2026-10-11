"""facts table: agent memory."""
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base


class Fact(Base):
    __tablename__ = "facts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("runs.id"))
    k: Mapped[str] = mapped_column(String(128))
    v: Mapped[str] = mapped_column(Text)
