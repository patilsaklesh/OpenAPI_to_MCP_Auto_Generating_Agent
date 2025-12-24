from mcp.client import MCPClient
from .a2a_protocol import OrderConfirmedMessage


class SchedulingAgent:
    def __init__(self, calendar_mcp_url: str):
        self.calendar_client = MCPClient(calendar_mcp_url)

    def handle_message(self, message: OrderConfirmedMessage):
        """
        Handle messages from Ordering Agent.
        """
        if isinstance(message, OrderConfirmedMessage):
            self._schedule_delivery(message)

    def _schedule_delivery(self, message: OrderConfirmedMessage):
        """
        Uses external MCP server (calendar/reminder).
        """
        self.calendar_client.call_tool(
            tool_name="createEvent",
            input={
                "title": f"Pizza Delivery ({message.order_id})",
                "minutes_from_now": message.eta_minutes
            }
        )

        print(
            f"[SchedulingAgent] Delivery scheduled for order {message.order_id}"
        )
