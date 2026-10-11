"""SSE service: in-memory per-run queues only."""
import asyncio
from collections import defaultdict
from backend.utils.logging import inside

_queues: dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)


def get_queue(run_id: str) -> asyncio.Queue:
    inside("get_queue", run_id)
    return _queues[run_id]


async def publish(run_id: str, event: dict) -> None:
    inside("publish", run_id)
    await _queues[run_id].put(event)
