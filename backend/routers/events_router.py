"""Events router: SSE stream tailed from the run trace file.

File tail (not the in-memory queue): _emit appends from worker threads and
asyncio.Queue.put_nowait is not thread-safe there, so the queue stays empty.
The trace file is the thread-safe transport; backlog drains on subscribe.
"""
import asyncio
import json
import os
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from backend.utils.logging import inside

router = APIRouter(prefix="/api/runs", tags=["events"])


@router.get("/{run_id}/events")
async def events(run_id: str):
    inside("events", run_id)
    path = os.path.abspath(os.path.join("runs", run_id, "trace.jsonl"))

    async def gen():
        sent, idle = 0, 0
        while True:
            lines = []
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()
            for line in lines[sent:]:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                yield {"event": event.get("type", "message"),
                       "data": json.dumps(event)}
                if event.get("type") == "done":
                    return
            idle = 0 if len(lines) > sent else idle + 1
            sent = len(lines)
            if idle >= 240:
                yield {"event": "timeout", "data": "idle 120s"}
                return
            await asyncio.sleep(0.5)

    return EventSourceResponse(gen())
