"""Generic document text extraction: PDFs and images. Pure functions, no DB/LLM."""
import os
from backend.agent.tools.files import resolve
from backend.utils.logging import inside

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")


def pdf_text(path: str, max_chars: int = 6000) -> str:
    inside("pdf_text", path)
    try:
        import pdfplumber
    except ImportError:
        return "pdf_text unavailable: pdfplumber is not installed"
    try:
        target = resolve(path)
    except ValueError as e:
        return f"refused: {e}"
    if not target.lower().endswith(".pdf") or not os.path.isfile(target):
        return f"not found: {os.path.basename(path)!r} (use file_list to see what's there)"
    try:
        with pdfplumber.open(target) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
    except OSError:
        return f"not found: {os.path.basename(path)!r} (use file_list to see what's there)"
    text = text.strip()
    if not text:
        return (f"no extractable text in {os.path.basename(path)!r}; "
                "try image_text for scanned pages")
    if len(text) > max_chars:
        text = text[:max_chars] + f"... [truncated {len(text) - max_chars} chars]"
    return text


def image_text(path: str) -> str:
    inside("image_text", path)
    try:
        target = resolve(path)
    except ValueError as e:
        return f"refused: {e}"
    if not os.path.isfile(target):
        return f"not found: {os.path.basename(path)!r} (use file_list to see what's there)"
    if not target.lower().endswith(IMAGE_EXTS):
        return (f"image_text needs an image file ({', '.join(IMAGE_EXTS)}); "
                "use pdf_text for PDFs, file_read for text files")
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        return ("ocr unavailable: install it with `pip install pillow pytesseract` "
                "plus the Tesseract binary (https://github.com/tesseract-ocr/tesseract), "
                "then restart the backend")
    try:
        return (pytesseract.image_to_string(Image.open(target)).strip()
                or "(no text detected)")[:6000]
    except Exception as e:
        return f"ocr failed: {e}"


SCHEMAS = [
    {"type": "function", "function": {
        "name": "pdf_text",
        "description": "Extract plain text from any PDF under an allowed root (resumes, reports, documents; use invoice_parse for invoices)",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "max_chars": {"type": "integer"}}, "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "image_text",
        "description": "OCR text from an image file (png/jpg) under an allowed root; needs Tesseract installed",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
]
