"""Events router: SSE placeholder (Phase 4 streams real steps)."""
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
from backend.utils.logging import inside

router = APIRouter(prefix="/api/runs", tags=["events"])


@router.get("/{run_id}/events")
async def events(run_id: str):
    inside("events", run_id)
    async def gen():
        yield {"event": "hello", "data": run_id}
        await asyncio.sleep(0.1)
    return EventSourceResponse(gen())
