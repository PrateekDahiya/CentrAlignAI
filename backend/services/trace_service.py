"""Trace service: append JSONL per run only."""
import os
import json


def append_trace(run_id: str, event: dict) -> None:
    d = os.path.join("runs", run_id)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "trace.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
