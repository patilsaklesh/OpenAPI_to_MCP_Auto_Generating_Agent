from utils.mcp_client import MCPClient

mcp = MCPClient("generated_mcp_server/server.py")

print("TOOLS:")
print(mcp.list_tools())

print("\nMENU:")
print(mcp.call_tool("list_menu", {}))


