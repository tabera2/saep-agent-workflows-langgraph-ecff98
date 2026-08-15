from langchain_core.tools import tool

ORDERS = {"A100": "shipped", "A200": "processing"}


@tool
def get_order_status(order_id: str) -> str:
    """Look up the shipping status of an order by its ID (format: a letter + 3 digits)."""
    order_id = order_id.strip().upper()
    if not (len(order_id) == 4 and order_id[0].isalpha() and order_id[1:].isdigit()):
        return f"ERROR: '{order_id}' is not a valid order id (expected e.g. A100)"
    status = ORDERS.get(order_id)
    if status is None:
        return f"ERROR: order {order_id} not found"
    return status


@tool
def create_ticket(summary: str) -> str:
    """Open a support ticket and return its reference number."""
    if not summary.strip():
        return "ERROR: summary must not be empty"
    return "TICKET-4821"


@tool
def escalate_to_human(reason: str) -> str:
    """Hand the conversation to a human agent with a reason."""
    if not reason.strip():
        return "ERROR: reason must not be empty"
    return "escalated"
