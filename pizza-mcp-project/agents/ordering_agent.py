
import os
import json
from groq import Groq
from typing import Optional, Dict, Any
from .a2a_protocol import OrderConfirmed


class OrderingAgent:
    
    def __init__(self, mcp_client, scheduling_agent=None):
        
        self.mcp_client = mcp_client
        self.scheduling_agent = scheduling_agent
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.conversation_history = []
        
        # Get available tools from MCP server
        self.tools = self.mcp_client.get_available_tools()
        
    def handle_user_input(self, user_input: str) -> Dict[str, Any]:
    
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Call Groq with function calling
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful pizza ordering assistant. 
                        You help users order pizzas by understanding their requests and calling the appropriate tools.
                        
                        Available pizzas: Margherita, Pepperoni, Veggie, Hawaiian
                        Available sizes: Small, Medium, Large
                        
                        When a user wants to order, use the placeOrder tool with pizza name, size, and quantity.
                        When a user wants to see the menu, use the getMenu tool.
                        When a user wants to track an order, use the trackOrder tool with their order_id.
                        
                        Be friendly and conversational."""
                    },
                    *self.conversation_history
                ],
                tools=self._convert_tools_to_groq_format(),
                tool_choice="auto",
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message
            
        
            if assistant_message.tool_calls:
                
                tool_results = []
                
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 Calling tool: {tool_name} with args: {tool_args}")
                    
                    # Call MCP
                    result = self.mcp_client.call_tool(tool_name, tool_args)
                    tool_results.append(result)
                    
                    # If this was a placeOrder call, notify scheduling agent
                    if tool_name == "placeOrder" and self.scheduling_agent and "order_id" in result:
                        order_msg = OrderConfirmed(
                            order_id=result["order_id"],
                            eta_minutes=result["eta_minutes"],
                            pizza=result.get("pizza", "Unknown"),
                            size=result.get("size", "Medium"),
                            quantity=result.get("quantity", 1)
                        )
                        
                        print(f"📨 Sending A2A message to Scheduling Agent...")
                        scheduling_result = self.scheduling_agent.handle_order(order_msg)
                        result["scheduling"] = scheduling_result
                
                # assistant's tool call history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in assistant_message.tool_calls
                    ]
                })
                
                # tool results to history
                for i, tool_call in enumerate(assistant_message.tool_calls):
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_results[i])
                    })
                
                final_response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=self.conversation_history,
                    max_tokens=500
                )
                
                final_message = final_response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
                
                return {
                    "response": final_message,
                    "tool_results": tool_results
                }
            else:
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content
                })
                
                return {
                    "response": assistant_message.content,
                    "tool_results": []
                }
                
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            print(f" {error_msg}")
            return {
                "response": error_msg,
                "tool_results": []
            }
    
    def _convert_tools_to_groq_format(self):
        """
        Convert MCP tool definitions to Groq function calling format.
        """
        groq_tools = []
        
        for tool in self.tools:
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"]
                }
            })
        
        return groq_tools