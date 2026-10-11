"""run_id helper only."""
import uuid
from backend.utils.logging import inside


def new_run_id() -> str:
    rid = str(uuid.uuid4())
    inside("new_run_id", rid)
    return rid
