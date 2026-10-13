"""Open a URL headless, return title + text. Screenshot to runs/."""
import os
import time
from backend.utils.logging import inside


def browser_open(url: str = "") -> str:
    inside("browser_open", url)
    if not url.startswith(("http://", "https://")):
        return "error: url must start with http"
    try:
        from playwright.sync_api import sync_playwright
        os.makedirs("runs", exist_ok=True)
        shot = os.path.join("runs", f"browser_{int(time.time())}.png")
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page()
            pg.goto(url, timeout=30000)
            title = pg.title()
            text = pg.inner_text("body")[:3000]
            pg.screenshot(path=shot)
            b.close()
    except Exception as e:
        return f"browser failed [{type(e).__name__}]: {e}"
    return f"title={title}\nshot={shot}\n{text}"


SCHEMAS = [
    {"type": "function", "function": {
        "name": "browser_open",
        "description": "Open a web page and read its text content",
        "parameters": {"type": "object", "properties": {
            "url": {"type": "string"}}, "required": ["url"]}}},
]
