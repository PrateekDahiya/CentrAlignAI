"""Pydantic schemas: invoices."""
from pydantic import BaseModel
from datetime import date


class InvoiceCreate(BaseModel):
    vendor: str
    invoice_no: str
    amount: float
    due_date: date | None = None
    source_file: str = ""


class InvoiceOut(InvoiceCreate):
    id: int
