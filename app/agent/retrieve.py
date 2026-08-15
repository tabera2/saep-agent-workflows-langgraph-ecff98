from app.agent.state import AgentState

# A tiny stand-in knowledge base. In production this is a vector store.
DOCS = {
    "refund": "Refunds are issued within 30 days of purchase to the original card.",
    "shipping": "Orders ship in 2 business days; tracking is emailed on dispatch.",
}


def retrieve(state: AgentState) -> dict:
    """RAG: find relevant docs and inject them as context before the model runs."""
    question = state["messages"][-1].content.lower()
    hits = [text for key, text in DOCS.items() if key in question]
    if not hits:
        return {}
    context = "Use ONLY these facts:\n" + "\n".join(hits)
    # Prepend the grounding context as a system message.
    return {"messages": [{"role": "system", "content": context}]}
