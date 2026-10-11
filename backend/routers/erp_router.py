"""ERP router: mock internal system CRUD (thin)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.db.session import get_db
from backend.models.invoice import Invoice
from backend.schemas.invoice_schema import InvoiceCreate, InvoiceOut
from backend.utils.logging import inside

router = APIRouter(prefix="/api/erp", tags=["erp"])


@router.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db)):
    inside("list_invoices", "-")
    return db.query(Invoice).order_by(Invoice.id.desc()).limit(100).all()


@router.post("/invoices", response_model=InvoiceOut)
def create_invoice(body: InvoiceCreate, db: Session = Depends(get_db)):
    inside("create_invoice", body.invoice_no)
    row = Invoice(**body.model_dump())
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(Invoice).filter_by(invoice_no=body.invoice_no).one()
        return existing
    db.refresh(row)
    return row
