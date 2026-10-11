"""run_id helper only."""
import uuid


def new_run_id() -> str:
    return str(uuid.uuid4())
