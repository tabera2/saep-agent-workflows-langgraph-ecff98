import time
import redis.asyncio as redis

r = redis.from_url("redis://localhost:6379")


def count_tool_calls(messages: list) -> int:
    """How many tool calls the model emitted across this turn's messages."""
    total = 0
    for m in messages:
        total += len(getattr(m, "tool_calls", None) or [])
    return total


async def record_turn(assistant_id: str, latency_ms: float, tool_calls: int) -> None:
    """Persist one turn's signals: a latency window plus running counters."""
    key = f"agent:{assistant_id}"
    # A capped rolling window of recent latencies for percentile math.
    await r.lpush(f"{key}:latency_ms", latency_ms)
    await r.ltrim(f"{key}:latency_ms", 0, 499)   # keep the last 500 turns
    # Monotonic counters — cheap to increment, cheap to read.
    await r.incr(f"{key}:turns")
    await r.incrby(f"{key}:tool_calls", tool_calls)
    # Publish so a live dashboard can react immediately.
    await r.publish("agent_turns", f"{assistant_id}:{latency_ms:.0f}:{tool_calls}")
