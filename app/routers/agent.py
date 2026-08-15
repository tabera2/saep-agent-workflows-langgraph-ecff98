from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.graph import build_graph

router = APIRouter(prefix="/agent", tags=["agent"])
_graph = build_graph()


class AgentTurn(BaseModel):
    message: str


@router.post("/{thread_id}/chat")
async def agent_chat(thread_id: str, body: AgentTurn) -> dict:
    """Run one agent turn within a persistent thread."""
    config = {"configurable": {"thread_id": thread_id}}
    out = _graph.invoke(
        {"messages": [("user", body.message)], "assistant_id": "support"},
        {**config, "recursion_limit": 8},
    )
    return {"answer": out["messages"][-1].content}
