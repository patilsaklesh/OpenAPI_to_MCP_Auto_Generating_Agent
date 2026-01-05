import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openapi_to_mcp.parser import load_openapi_spec
from openapi_to_mcp.transformer import openapi_to_ir
from openapi_to_mcp.mcp_generator import generate_mcp_server
from utils.mcp_client import MCPClient, CalendarMCPClient
from agents.ordering_agent import OrderingAgent
from agents.scheduling_agent import SchedulingAgent
load_dotenv() 

def setup_system():
    #phase1
    base_dir = Path(__file__).parent              # openapi_to_mcp
    project_root = base_dir.parent                # pizza-mcp-project
    
    openapi_file = project_root / "openapi" / "pizza_api.yaml"
    output_dir = project_root / "generated_mcp_server"
    
    # generate MCP server
    openapi_spec = load_openapi_spec(openapi_file)
    service_ir = openapi_to_ir(openapi_spec)
    generate_mcp_server(service_ir, output_dir)
    
    return output_dir / "server.py"

def run_demo(pizza_mcp_path):
    
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: GROQ_API_KEY not found")
        sys.exit(1)
    
    # MCP clients (connecting to actual servers)
    pizza_mcp_client = MCPClient(str(pizza_mcp_path))
    calendar_mcp_client = CalendarMCPClient(str(calendar_mcp_path))
    
    # ✅ Initialize agents in correct order
    scheduling_agent = SchedulingAgent(calendar_mcp_client)
    ordering_agent = OrderingAgent(pizza_mcp_client, scheduling_agent)
    
    #Interactive loop
    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        
        result = ordering_agent.handle_user_input(user_input)
        print(f"\n🤖 Assistant: {result['response']}\n")

def main():
    pizza_mcp_path = setup_system()  
    run_demo(pizza_mcp_path)         

if __name__ == "__main__":
    main()