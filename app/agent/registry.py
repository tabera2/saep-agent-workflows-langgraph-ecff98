from dataclasses import dataclass
from app.agent.tools import get_order_status, create_ticket, escalate_to_human


@dataclass(frozen=True)
class ToolSpec:
    """A tool plus the metadata the graph uses to govern it."""
    fn: object        # the @tool-decorated callable
    risk: str         # "read" (safe) or "write" (needs approval)


# One registry is the single source of truth for what tools exist and how
# dangerous each is. Adding a tool here is the ONLY place you touch.
REGISTRY: dict[str, ToolSpec] = {
    "get_order_status": ToolSpec(get_order_status, risk="read"),
    "create_ticket": ToolSpec(create_ticket, risk="write"),
    "escalate_to_human": ToolSpec(escalate_to_human, risk="write"),
}

# The flat list LangGraph still needs to bind/execute.
TOOLS = [spec.fn for spec in REGISTRY.values()]

# The names that must pause for human approval before they run.
WRITE_TOOLS = [name for name, spec in REGISTRY.items() if spec.risk == "write"]


def requested_write_tool(message) -> bool:
    """True if the model's last message asks for any write-risk tool."""
    for call in getattr(message, "tool_calls", None) or []:
        if call["name"] in WRITE_TOOLS:
            return True
    return False
