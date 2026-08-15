from app.agent.graph import build_graph

_graph = build_graph()


def start(question: str, thread_id: str) -> dict:
    """Run until the graph pauses before a tool (or finishes)."""
    config = {"configurable": {"thread_id": thread_id}}
    return _graph.invoke({"messages": [("user", question)],
                          "assistant_id": "support"}, config)


def pending_tool(thread_id: str):
    """The tool call the graph is paused on, if any."""
    config = {"configurable": {"thread_id": thread_id}}
    state = _graph.get_state(config)
    last = state.values["messages"][-1]
    return getattr(last, "tool_calls", None)


def approve(thread_id: str) -> dict:
    """Resume the paused graph, letting the pending tool run."""
    config = {"configurable": {"thread_id": thread_id}}
    return _graph.invoke(None, config)  # None = continue from the checkpoint
