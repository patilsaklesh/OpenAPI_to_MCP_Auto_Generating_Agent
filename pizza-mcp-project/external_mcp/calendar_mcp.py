"""
Mock Calendar MCP Server
-----------------------
This simulates an external MCP-enabled service (e.g., Google Calendar).
Used by the Scheduling Agent to schedule pizza delivery reminders.
"""

from mcp.server import MCPServer
import datetime

server = MCPServer()

@server.tool()
def createEvent(input: dict) -> dict:
    """
    Create a calendar event after a given number of minutes.
    """
    title = input.get("title", "Untitled Event")
    minutes_from_now = input.get("minutes_from_now", 0)

    event_time = datetime.datetime.now() + datetime.timedelta(
        minutes=minutes_from_now
    )

    return {
        "event_id": f"event-{int(event_time.timestamp())}",
        "title": title,
        "scheduled_time": event_time.isoformat()
    }


if __name__ == "__main__":
    server.run()
