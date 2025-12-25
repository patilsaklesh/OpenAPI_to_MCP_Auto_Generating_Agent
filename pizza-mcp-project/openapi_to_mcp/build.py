from .parser import load_openapi_spec
from .transformer import openapi_to_ir
from .mcp_generator import generate_mcp_server
from pathlib import Path


def main():
    base_dir = Path(__file__).parent              # openapi_to_mcp/
    project_root = base_dir.parent                # pizza-mcp-project/

    openapi_file = project_root / "OpenAPI" / "pizza_api.yaml"
    output_dir = project_root / "generated_mcp_server"
    
    openapi_spec = load_openapi_spec(openapi_file)
    service_ir = openapi_to_ir(openapi_spec)

    generate_mcp_server(service_ir, output_dir)


if __name__ == "__main__":
    main()
