"""Tool registry: bound tools + schemas. Single import point for loop."""
from backend.utils.logging import inside


def build_tools(db, run_id: str):
    """Bind db/run_id into closures. Returns (tools dict, schemas list)."""
    inside("build_tools", run_id)
    from backend.agent.tools import files, invoice_parse, erp_tools
    from backend.agent.tools import web_search, browser_open, ask_user, doc_text
    tools = {
        "file_list": files.file_list,
        "file_read": files.file_read,
        "pdf_text": doc_text.pdf_text,
        "image_text": doc_text.image_text,
        "invoice_parse": invoice_parse.invoice_parse,
        "web_search": web_search.web_search,
        "browser_open": browser_open.browser_open,
        "erp_list": lambda vendor="": erp_tools.erp_list(db, vendor),
        "erp_create": lambda vendor="", invoice_no="", amount=0.0, due_date="", source_file="": erp_tools.erp_create(db, vendor, invoice_no, amount, due_date, source_file),
        "ask_user": lambda question="": ask_user.ask_user(db, run_id, question),
    }
    schemas = (files.SCHEMAS + doc_text.SCHEMAS + invoice_parse.SCHEMAS + web_search.SCHEMAS
                + browser_open.SCHEMAS + erp_tools.SCHEMAS + ask_user.SCHEMAS)
    return tools, schemas
