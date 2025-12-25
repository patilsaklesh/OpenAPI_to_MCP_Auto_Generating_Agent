from pathlib import Path
import yaml


def load_openapi_spec(path) -> dict:
    """
    Load an OpenAPI YAML file and return it as a Python dictionary.
    """
    spec_path = Path(path)

    if not spec_path.exists():
        raise FileNotFoundError(f"OpenAPI spec not found: {path}")

    with open(spec_path, "r") as f:
        return yaml.safe_load(f)
