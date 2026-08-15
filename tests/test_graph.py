from langchain_core.messages import AIMessage
from app.agent import graph as graph_mod
from app.agent.state import AgentState


class FakeModel:
    """A stand-in chat model: no network, returns a fixed reply with no tool call."""
    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        return AIMessage(content="Refunds are within 30 days.")


def test_graph_answers_without_tools(monkeypatch):
    monkeypatch.setattr(graph_mod, "model", FakeModel())
    g = graph_mod.build_graph()
    out = g.invoke(
        {"messages": [("user", "What is the refund window?")],
         "assistant_id": "support"},
        {"configurable": {"thread_id": "t1"}, "recursion_limit": 8},
    )
    assert "30 days" in out["messages"][-1].content


def test_retrieve_grounds_on_keyword():
    state: AgentState = {"messages": [("user", "refund please")],
                         "assistant_id": "support"}
    from app.agent.retrieve import retrieve
    update = retrieve(state)  # type: ignore[arg-type]
    assert "30 days" in update["messages"][0]["content"]
