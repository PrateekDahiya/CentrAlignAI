"""Local file tools under allowed roots. Pure functions, no DB/LLM."""
import os
from backend.config import settings
from backend.utils.logging import inside

INBOX = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "inbox"))

def _root_abspath(r: str) -> str:
    # Bare "D:" means cwd-on-D on Windows, not the drive root.
    if len(r) == 2 and r[1] == ":" and r[0].isalpha():
        r += os.sep
    return os.path.abspath(r)


ROOTS = [_root_abspath(r) for r in settings.file_roots] or [INBOX]

SENSITIVE_SUFFIXES = (".pem", ".key",)
SENSITIVE_PARTS = ("id_rsa",)


def _sensitive(base: str) -> bool:
    low = base.lower()
    if low == ".env.example":
        return False
    return (low == ".env" or low.startswith(".env.")
            or low.endswith(SENSITIVE_SUFFIXES)
            or any(p in low for p in SENSITIVE_PARTS))


def resolve(name: str) -> str:
    """Absolute or inbox-relative path; must sit under an allowed root."""
    p = os.path.abspath(name if os.path.isabs(name) else os.path.join(INBOX, name))
    if _sensitive(os.path.basename(p)):
        raise ValueError(f"refused: sensitive file {name!r}")
    if not any(p == r or p.startswith(r.rstrip(os.sep) + os.sep) for r in ROOTS):
        raise ValueError(
            f"path outside allowed roots {name!r}; ask the user to add it "
            "to FILE_ROOTS in .env and restart the backend, or to supply "
            "the files another way")
    return p


def file_list(directory: str = "") -> str:
    inside("file_list", directory or "inbox")
    if not directory:
        names = sorted(os.listdir(INBOX))
        return "files: " + (", ".join(names) if names else "(empty)")
    try:
        base = resolve(directory)
    except ValueError as e:
        return f"refused: {e}"
    if not os.path.isdir(base):
        return (f"no such directory {directory!r}; relative names resolve "
                f"under inbox ({INBOX}); otherwise pass a full absolute path.")
    names = sorted(os.listdir(base))
    return "files: " + (", ".join(names) if names else "(empty)")


def file_read(path: str) -> str:
    inside("file_read", path)
    if path.lower().endswith(".pdf"):
        return "hint: use invoice_parse for PDFs"
    try:
        with open(resolve(path), encoding="utf-8", errors="replace") as f:
            return f.read(4000)
    except ValueError as e:
        return f"refused: {e}"
    except OSError:
        return f"not found: {os.path.basename(path)!r} (use file_list to see what's there)"


SCHEMAS = [
    {"type": "function", "function": {
        "name": "file_list",
        "description": "List files under an allowed root (inbox by default; absolute paths under FILE_ROOTS also work)",
        "parameters": {"type": "object", "properties": {
            "directory": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {
        "name": "file_read",
        "description": "Read a text file under an allowed root (not PDFs, not secrets)",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}}},
]
