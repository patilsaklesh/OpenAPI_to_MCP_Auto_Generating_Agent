from typing import Dict
from mcp.client import MCPClient
from .a2a_protocol import OrderConfirmedMessage


class OrderingAgent:
    def __init__(self, mcp_server_url: str, scheduling_agent):
        self.mcp_client = MCPClient(mcp_server_url)
        self.scheduling_agent = scheduling_agent

    def handle_user_input(self, user_input: str):
        """
        Entry point for user commands.
        """
        if "pizza" in user_input.lower():
            return self._place_order()
        else:
            return {"message": "Sorry, I can only help with pizza orders."}

    def _place_order(self) -> Dict:
        """
        Calls MCP tool to place an order.
        """
        response = self.mcp_client.call_tool(
            tool_name="placeOrder",
            input={
                "pizza": "Margherita",
                "size": "Large",
                "quantity": 1
            }
        )

        order_id = response["order_id"]
        eta = response["eta_minutes"]

        # Send message to scheduling agent
        msg = OrderConfirmedMessage(order_id, eta)
        self.scheduling_agent.handle_message(msg)

        return {
            "message": "Order placed successfully",
            "order_id": order_id,
            "eta_minutes": eta
        }
