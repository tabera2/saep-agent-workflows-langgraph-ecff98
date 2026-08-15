from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """The data that flows through the graph and accumulates each step."""
    # `add_messages` is a reducer: new messages are APPENDED, not replaced.
    messages: Annotated[list, add_messages]
    assistant_id: str
