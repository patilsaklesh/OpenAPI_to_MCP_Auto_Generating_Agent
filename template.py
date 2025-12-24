import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Project root name
project_name = "pizza-mcp-project"

# List of files & folders to create
list_of_files = [

    # OpenAPI input
    f"{project_name}/openapi/pizza_api.yaml",

    # OpenAPI → MCP core logic
    f"{project_name}/openapi_to_mcp/__init__.py",
    f"{project_name}/openapi_to_mcp/parser.py",
    f"{project_name}/openapi_to_mcp/ir.py",
    f"{project_name}/openapi_to_mcp/transformer.py",
    f"{project_name}/openapi_to_mcp/mcp_generator.py",

    # Generated MCP server (auto-generated output)
    f"{project_name}/generated_mcp_server/__init__.py",
    f"{project_name}/generated_mcp_server/server.py",
    f"{project_name}/generated_mcp_server/README.md",

    # Agents
    f"{project_name}/agents/__init__.py",
    f"{project_name}/agents/ordering_agent.py",
    f"{project_name}/agents/scheduling_agent.py",
    f"{project_name}/agents/a2a_protocol.py",

    # External MCP (mock or real)
    f"{project_name}/external_mcp/__init__.py",
    f"{project_name}/external_mcp/calendar_mcp.py",

    # Entry point & docs
    f"{project_name}/main.py",
    f"{project_name}/README.md",
    f"{project_name}/architecture.md",

    # Optional extras
    f"{project_name}/requirements.txt",
    f"{project_name}/.gitignore"
]

# Create files & directories
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created empty file: {filepath}")

    else:
        logging.info(f"File already exists: {filepath}")
