from typing import Dict
from .ir import ToolIR, ServiceIR


def openapi_to_ir(openapi_spec: Dict) -> ServiceIR:
    """
    Convert OpenAPI specification to Intermediate Representation (IR).
    """
    service_name = openapi_spec["info"]["title"]
    tools = []

    paths = openapi_spec.get("paths", {})

    for path, methods in paths.items():
        for http_method, meta in methods.items():
            tool_name = meta.get("operationId")
            if not tool_name:
                continue 

            description = meta.get("summary", "")

           
            input_schema = {}
            if "requestBody" in meta:
                content = meta["requestBody"]["content"]
                if "application/json" in content:
                    input_schema = content["application/json"]["schema"]

            
            output_schema = {}
            responses = meta.get("responses", {})
            if "200" in responses:
                content = responses["200"].get("content", {})
                if "application/json" in content:
                    output_schema = content["application/json"]["schema"]

            tools.append(
                ToolIR(
                    name=tool_name,
                    description=description,
                    input_schema=input_schema,
                    output_schema=output_schema,
                )
            )

    return ServiceIR(service_name=service_name, tools=tools)
