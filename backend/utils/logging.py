"""Logger with run_id correlation + entry helper. No project imports (leaf)."""
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")


def get_logger(run_id: str = "-") -> logging.LoggerAdapter:
    return logging.LoggerAdapter(logging.getLogger("worker"), {"run_id": run_id})


def inside(method: str, identifier: object = "-") -> None:
    """Method-entry log. Format: inside {method} for {identifier}."""
    text = str(identifier)
    if len(text) > 80:
        text = text[:80] + "..."
    logging.getLogger("worker").info(f"inside {method} for {text}")
