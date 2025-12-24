"""
Demo Entry Point
----------------
Runs a simple CLI demo:
User -> Ordering Agent -> Pizza MCP -> Scheduling Agent -> Calendar MCP
"""

from agents.ordering_agent import OrderingAgent
from agents.scheduling_agent import SchedulingAgent


def main():
    print("=== Pizza MCP Demo ===")
    print("Type your request (e.g., 'I need a pizza')")
    print("Type 'exit' to quit.\n")

    # URLs where MCP servers are running
    PIZZA_MCP_URL = "http://localhost:8000"
    CALENDAR_MCP_URL = "http://localhost:8001"

    # Initialize agents
    scheduling_agent = SchedulingAgent(calendar_mcp_url=CALENDAR_MCP_URL)
    ordering_agent = OrderingAgent(
        mcp_server_url=PIZZA_MCP_URL,
        scheduling_agent=scheduling_agent
    )

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting demo.")
            break

        response = ordering_agent.handle_user_input(user_input)
        print("\n[Agent Response]")
        print(response)
        print()


if __name__ == "__main__":
    main()
