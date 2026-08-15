from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.redis import RedisSaver
from langchain_openai import ChatOpenAI
from app.agent.state import AgentState
from app.agent.registry import TOOLS, WRITE_TOOLS, requested_write_tool
from app.agent.retrieve import retrieve

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).bind_tools(TOOLS)


def call_model(state: AgentState) -> dict:
    reply = model.invoke(state["messages"])
    return {"messages": [reply]}


def route_after_assistant(state: AgentState) -> str:
    """Read tools → run now; write tools → pause for approval; else finish."""
    last = state["messages"][-1]
    if not getattr(last, "tool_calls", None):
        return END
    return "approve" if requested_write_tool(last) else "tools"


def build_graph(redis_url: str = "redis://localhost:6379"):
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("assistant", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    # A second tool node used only on the approval path.
    graph.add_node("approve", ToolNode(TOOLS))
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "assistant")
    graph.add_conditional_edges("assistant", route_after_assistant)
    graph.add_edge("tools", "assistant")
    graph.add_edge("approve", "assistant")
    checkpointer = RedisSaver.from_conn_string(redis_url)
    # Only the approval path pauses — safe reads never block a user.
    return graph.compile(checkpointer=checkpointer, interrupt_before=["approve"])
