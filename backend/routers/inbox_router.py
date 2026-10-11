"""Inbox router: list fake invoice PDFs (thin)."""
import os
from fastapi import APIRouter

router = APIRouter(prefix="/api/inbox", tags=["inbox"])
INBOX = os.path.join(os.path.dirname(__file__), "..", "..", "data", "inbox")


@router.get("/files")
def list_files():
    path = os.path.abspath(INBOX)
    if not os.path.isdir(path):
        return []
    return sorted(f for f in os.listdir(path) if f.lower().endswith(".pdf"))
