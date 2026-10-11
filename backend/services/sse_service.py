"""SSE service: in-memory per-run queues only."""
import asyncio
from collections import defaultdict

_queues: dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)


def get_queue(run_id: str) -> asyncio.Queue:
    return _queues[run_id]


async def publish(run_id: str, event: dict) -> None:
    await _queues[run_id].put(event)
