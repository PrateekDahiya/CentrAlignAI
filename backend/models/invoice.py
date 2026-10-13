"""erp_invoices table: mock internal system."""
from sqlalchemy import String, Numeric, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base


class Invoice(Base):
    __tablename__ = "erp_invoices"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vendor: Mapped[str] = mapped_column(String(128))
    invoice_no: Mapped[str] = mapped_column(String(64), unique=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    due_date: Mapped[str] = mapped_column(Date, nullable=True)
    source_file: Mapped[str] = mapped_column(String(256), default="")
    source: Mapped[str] = mapped_column(String(20), default="invoice")
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
