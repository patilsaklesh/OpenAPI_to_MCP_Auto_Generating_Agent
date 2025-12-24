from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class ToolIR:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


@dataclass
class ServiceIR:
    service_name: str
    tools: List[ToolIR]
