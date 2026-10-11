"""Trace router: download run trace (thin)."""
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from backend.utils.logging import inside

router = APIRouter(prefix="/api/runs", tags=["trace"])


@router.get("/{run_id}/trace")
def get_trace(run_id: str):
    inside("get_trace", run_id)
    path = os.path.abspath(os.path.join("runs", run_id, "trace.jsonl"))
    if not os.path.exists(path):
        return {"run_id": run_id, "steps": []}
    return FileResponse(path, media_type="application/jsonl", filename="trace.jsonl")
