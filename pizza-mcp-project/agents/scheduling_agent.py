from typing import Dict, Any
from .a2a_protocol import OrderConfirmed, SchedulingComplete

class SchedulingAgent:
    def __init__(self, calendar_mcp_client): 
        self.calendar_client = calendar_mcp_client

    def handle_order(self, order_msg: OrderConfirmed) -> SchedulingComplete:
        """Handle incoming order and schedule delivery"""
        
       
        event_title = f"Pizza Delivery - Order #{order_msg.order_id}"
        
        result = self.calendar_client.create_event(
            title=event_title,
            minutes_from_now=order_msg.eta_minutes
        )
        
      
        return SchedulingComplete(
            order_id=order_msg.order_id,
            event_id=result.get("event_id", "unknown"),
            scheduled_time=result.get("scheduled_time", "unknown"),
            status="Delivery reminder scheduled successfully"
        )