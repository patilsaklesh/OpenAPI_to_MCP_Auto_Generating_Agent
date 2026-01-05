import subprocess
import json
import sys
from typing import Dict, List, Any


class MCPClient:
    
    def __init__(self, server_script_path: str):
        """
        Initialize MCP client with path to server script.
        
        Args:
            server_script_path: Path to the MCP server Python file
        """
        self.server_script_path = server_script_path
        self.available_tools = []
        
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools from the MCP server.
        This simulates the tools/list MCP protocol call.
        """
        # For simplicity, we'll parse the server file to extract tool definitions
        # In a real implementation, you'd use proper MCP protocol
        
        # Return mock tool definitions based on our pizza API
        self.available_tools = [
            {
                "name": "getMenu",
                "description": "Get pizza menu",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "placeOrder",
                "description": "Place a pizza order",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pizza": {"type": "string", "description": "Name of the pizza"},
                        "size": {"type": "string", "description": "Size: Small, Medium, or Large"},
                        "quantity": {"type": "integer", "description": "Number of pizzas"}
                    },
                    "required": ["pizza", "size", "quantity"]
                }
            },
            {
                "name": "trackOrder",
                "description": "Track an order by order ID",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The order ID to track"}
                    },
                    "required": ["order_id"]
                }
            }
        ]
        
        return self.available_tools
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool and return the result.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments for the tool
            
        Returns:
            Tool execution result as a dictionary
        """
        try:
           
            cmd = [
                sys.executable,
                self.server_script_path,
                tool_name,
                json.dumps(arguments)
            ]
            
            
            import importlib.util
            spec = importlib.util.spec_from_file_location("mcp_server", self.server_script_path)
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)
            
            
            if hasattr(server_module, tool_name):
                tool_func = getattr(server_module, tool_name)
                result = tool_func(**arguments)
                return result
            else:
                return {"error": f"Tool {tool_name} not found"}
                
        except Exception as e:
            return {"error": str(e)}


class CalendarMCPClient:
    """
    Client for external Calendar MCP server.
    """
    
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        
    def create_event(self, title: str, minutes_from_now: int) -> Dict[str, Any]:
        """
        Create a calendar event.
        
        Args:
            title: Event title
            minutes_from_now: Minutes from now to schedule the event
            
        Returns:
            Event creation result
        """
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("calendar_mcp", self.server_script_path)
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)
            
            if hasattr(server_module, 'createEvent'):
                tool_func = getattr(server_module, 'createEvent')
                result = tool_func(
                    title=title,
                    minutes_from_now=minutes_from_now
                )
                return result
            else:
                return {"error": "createEvent tool not found"}
                
        except Exception as e:
            return {"error": str(e)}