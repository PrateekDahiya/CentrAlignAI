"""Logger with run_id correlation, nothing else."""
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")


def get_logger(run_id: str = "-") -> logging.LoggerAdapter:
    return logging.LoggerAdapter(logging.getLogger("worker"), {"run_id": run_id})
