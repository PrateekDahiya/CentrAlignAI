"""Local inbox file tools. Pure functions, no DB/LLM."""
import os
from backend.utils.logging import inside

INBOX = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "inbox"))


def resolve(name: str) -> str:
    """Inbox-relative path, rejects traversal outside INBOX."""
    p = os.path.abspath(os.path.join(INBOX, name))
    if not p.startswith(INBOX):
        raise ValueError("path outside inbox")
    return p


def file_list(directory: str = "") -> str:
    inside("file_list", directory or "inbox")
    base = resolve(directory) if directory else INBOX
    if not os.path.isdir(base):
        base = INBOX
        note = f"no such subdir {directory!r}; showing inbox. "
    else:
        note = ""
    names = sorted(os.listdir(base))
    return note + "files: " + (", ".join(names) if names else "(empty)")


def file_read(path: str) -> str:
    inside("file_read", path)
    if path.lower().endswith(".pdf"):
        return "hint: use invoice_parse for PDFs"
    with open(resolve(path), encoding="utf-8", errors="replace") as f:
        return f.read(4000)


SCHEMAS = [
    {"type": "function", "function": {
        "name": "file_list",
        "description": "List files in the invoice inbox directory",
        "parameters": {"type": "object", "properties": {
            "directory": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {
        "name": "file_read",
        "description": "Read a text file from the inbox (not PDFs)",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
]
