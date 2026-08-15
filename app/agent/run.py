import time
from app.agent.graph import build_graph
from app.agent.metrics import record_turn, count_tool_calls

_graph = build_graph()


async def run_turn(question: str, assistant_id: str = "support",
                   thread_id: str = "default") -> str:
    """Run one turn, then record its latency and tool-call count."""
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 8}
    started = time.perf_counter()
    out = _graph.invoke(
        {"messages": [("user", question)], "assistant_id": assistant_id},
        config,
    )
    latency_ms = (time.perf_counter() - started) * 1000
    await record_turn(assistant_id, latency_ms, count_tool_calls(out["messages"]))
    return out["messages"][-1].content
