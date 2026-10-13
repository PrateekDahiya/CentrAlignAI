"""ERP tools: MySQL CRUD. db passed in, never global."""
from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.models.invoice import Invoice
from backend.utils.logging import inside


def _fmt(r: Invoice) -> str:
    return (f"id={r.id} vendor={r.vendor} invoice_no={r.invoice_no} "
            f"amount={float(r.amount):.2f} due_date={r.due_date} "
            f"source_file={r.source_file} source={r.source}")


def erp_list(db: Session, vendor: str = "") -> str:
    inside("erp_list", vendor or "-")
    q = db.query(Invoice)
    if vendor:
        q = q.filter(Invoice.vendor.ilike(f"%{vendor}%"))
    rows = q.order_by(Invoice.id.desc()).limit(20).all()
    return "invoices:\n" + "\n".join(_fmt(r) for r in rows) if rows else "invoices: (none)"


def erp_create(db: Session, vendor: str = "", invoice_no: str = "",
               amount: float = 0, due_date: str = "",
               source_file: str = "", source: str = "") -> str:
    inside("erp_create", invoice_no or "-")
    if not invoice_no or not amount:
        return "error: invoice_no and amount required"
    due = None
    if due_date:
        y, m, d = map(int, due_date.split("-"))
        due = date(y, m, d)
    row = Invoice(vendor=vendor or "?", invoice_no=invoice_no,
                  amount=amount, due_date=due, source_file=source_file,
                  source=source or "invoice")
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        row = db.query(Invoice).filter_by(invoice_no=invoice_no).one()
        return "duplicate (existing): " + _fmt(row)
    db.refresh(row)
    return "created: " + _fmt(row)


SCHEMAS = [
    {"type": "function", "function": {
        "name": "erp_list",
        "description": "List ERP invoices, optionally filtered by vendor",
        "parameters": {"type": "object", "properties": {
            "vendor": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {
        "name": "erp_create",
        "description": "Enter an invoice into the ERP system (source: 'invoice' for parsed PDFs/files, 'web_search' for web prices)",
        "parameters": {"type": "object", "properties": {
            "vendor": {"type": "string"}, "invoice_no": {"type": "string"},
            "amount": {"type": "number"}, "due_date": {"type": "string"},
            "source_file": {"type": "string"}, "source": {"type": "string"}},
            "required": ["invoice_no", "amount"]}}},
]
