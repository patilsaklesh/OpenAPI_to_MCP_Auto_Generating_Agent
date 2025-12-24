from pathlib import Path
from .ir import ServiceIR


def generate_mcp_server(service_ir: ServiceIR, output_dir: str):
    """
    Generate an MCP server Python file from ServiceIR.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    server_file = output_path / "server.py"

    with open(server_file, "w") as f:
        f.write("from mcp.server import MCPServer\n\n")
        f.write("server = MCPServer()\n\n")

        for tool in service_ir.tools:
            f.write(f"@server.tool()\n")
            f.write(f"def {tool.name}(input: dict) -> dict:\n")
            f.write(f"    \"\"\"{tool.description}\"\"\"\n")
            f.write(f"    # TODO: Implement backend logic\n")
            f.write(f"    return {{}}\n\n")

        f.write("\nif __name__ == '__main__':\n")
        f.write("    server.run()\n")
