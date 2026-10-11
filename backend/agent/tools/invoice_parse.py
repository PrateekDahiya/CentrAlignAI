"""Parse invoice PDFs. Pure function, no DB/LLM."""
import os
import re
import pdfplumber
from backend.utils.logging import inside
from backend.agent.tools.files import resolve


def invoice_parse(path: str) -> str:
    inside("invoice_parse", path)
    p = resolve(path)
    with pdfplumber.open(p) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    no = re.search(r"INV[-\s]?\d+", text)
    amt = re.search(r"Amount:\s*\$\s*([\d,]+\.\d{2})", text)
    due = re.search(r"Due date:\s*(\d{4}-\d{2}-\d{2})", text)
    vendor = re.search(r"Vendor:\s*(.+)", text)
    if not (no and amt):
        return f"unparsed: no invoice_no/amount in {path}"
    return (f"vendor={(vendor.group(1).strip() if vendor else '?')} "
            f"invoice_no={no.group(0).replace(' ', '-')} "
            f"amount={float(amt.group(1).replace(',', '')):.2f} "
            f"due_date={due.group(1) if due else ''} "
            f"source_file={os.path.basename(p)}")


SCHEMAS = [
    {"type": "function", "function": {
        "name": "invoice_parse",
        "description": "Extract vendor, invoice_no, amount, due_date from an inbox PDF",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
]
