"""Generate 3 fake invoice PDFs (no real data)."""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

INBOX = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "inbox"))

FAKES = [
    ("Acme_Corp_INV-1001.pdf", "Acme Corp", "INV-1001", "4,200.00", "2026-10-20"),
    ("Acme_Corp_INV-1002.pdf", "Acme Corp", "INV-1002", "7,850.50", "2026-11-05"),
    ("Globex_INV-2001.pdf", "Globex", "INV-2001", "1,230.00", "2026-10-28"),
]


def make_pdfs() -> list[str]:
    os.makedirs(INBOX, exist_ok=True)
    made = []
    for fname, vendor, no, amt, due in FAKES:
        path = os.path.join(INBOX, fname)
        c = canvas.Canvas(path, pagesize=LETTER)
        c.drawString(72, 720, f"INVOICE {no}")
        c.drawString(72, 700, f"Vendor: {vendor}")
        c.drawString(72, 680, f"Amount: ${amt}")
        c.drawString(72, 660, f"Due date: {due}")
        c.save()
        made.append(path)
    return made


if __name__ == "__main__":
    print(make_pdfs())
