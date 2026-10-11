"""steps table: agent trace."""
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base


class Step(Base):
    __tablename__ = "steps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("runs.id"))
    n: Mapped[int] = mapped_column(Integer)
    thought: Mapped[str] = mapped_column(Text, default="")
    tool: Mapped[str] = mapped_column(String(64), default="")
    args_json: Mapped[str] = mapped_column(Text, default="{}")
    obs: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
