"""Open a URL headless, return title + text. Screenshot to runs/."""
import os
import time
from backend.utils.logging import inside


UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")


def browser_open(url: str = "") -> str:
    inside("browser_open", url)
    if not url.startswith(("http://", "https://")):
        return "error: url must start with http"
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ("browser failed [import]: playwright is not installed "
                "(pip install playwright; python -m playwright install chromium)")
    os.makedirs("runs", exist_ok=True)
    shot = os.path.join("runs", f"browser_{int(time.time())}.png")
    try:
        with sync_playwright() as p:
            try:
                b = p.chromium.launch(headless=True)
            except Exception as e:
                return f"browser failed [launch {type(e).__name__}]: {e}"
            try:
                pg = b.new_page(user_agent=UA, locale="en-US",
                                viewport={"width": 1366, "height": 768})
                try:
                    pg.goto(url, timeout=30000)
                except Exception as e:
                    return f"browser failed [goto {type(e).__name__}]: {e}"
                title = pg.title()
                text = pg.inner_text("body")[:3000]
                pg.screenshot(path=shot)
            finally:
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
