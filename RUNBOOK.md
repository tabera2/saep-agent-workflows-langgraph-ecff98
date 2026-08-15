# Agent workflow runbook

## Invoking the agent
The compiled graph is stateful per **thread**. Pass a `thread_id` in config:

    graph = build_graph()
    config = {"configurable": {"thread_id": "user-42"}}
    out = graph.invoke({"messages": [("user", "Where is order A100?")],
                        "assistant_id": "support"}, config)

Re-invoking with the same `thread_id` continues the same conversation — Redis
holds the checkpoint.

## Health
- Liveness: the graph compiles and Redis `PING` returns PONG.
- If answers ignore your docs, confirm the `retrieve` node ran (it sits on the
  `START -> retrieve -> assistant` path) and that a doc key matched.

## Common incidents
- **Agent "forgets" mid-conversation**: a different `thread_id` was passed, or
  Redis was flushed — checkpoints live there, not in process memory.
- **Tool loop never ends**: the model keeps requesting tools; cap recursion with
  `graph.invoke(..., {"recursion_limit": 8})`.
- **Stuck waiting for approval**: a graph paused at `interrupt_before=["tools"]`
  never got an approve/reject — resume or roll back the thread.
- **Stale facts**: the RAG `DOCS` / vector store is out of date — re-index it.
