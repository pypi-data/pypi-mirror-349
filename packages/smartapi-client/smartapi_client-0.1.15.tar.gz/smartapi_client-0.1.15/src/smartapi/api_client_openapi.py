import json
import yaml
import re
import logging
from dataclasses import asdict, dataclass
from typing import List, Dict, Any, Tuple, Type

from smartapi.utils import normalize_method_name  # Assuming this is available

logger = logging.getLogger(__name__)


@dataclass
class Endpoint:
    name: str
    method: str
    path: str
    description: str


@classmethod
def from_openapi_spec(cls: Type['ApiClient'],
                      spec_path: str,
                      save_endpoints: bool = False,
                      path: str = ".",
                      file_name: str = "endpoints.json",
                      output_format: str = "json",
                      **kwargs) -> 'ApiClient':
    endpoints, metadata = cls._parse_openapi_spec(
        spec_path, save_endpoints=save_endpoints,
        save_path=path, file_name=file_name,
        output_format=output_format
    )

    api_name = kwargs.pop("api_name", metadata.get("api_name", "UnnamedAPI"))
    base_url = kwargs.pop("base_url", metadata.get("base_url", ""))

    client = cls(api_name=api_name, base_url=base_url, **kwargs)
    client.register_endpoints(endpoints)
    return client


@staticmethod
def _parse_openapi_spec(spec_path: str,
                        save_endpoints: bool = False,
                        save_path: str = ".",
                        file_name: str = "endpoints.json",
                        output_format: str = "json") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:

    def resolve_ref(ref: str, spec: Dict[str, Any]) -> Any:
        parts = ref.lstrip('#/').split('/')
        value = spec
        for part in parts:
            value = value.get(part, {})
        return value

    try:
        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f) if spec_path.endswith(
                ('.yaml', '.yml')) else json.load(f)
    except (IOError, yaml.YAMLError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse OpenAPI spec: {e}")

    api_name = spec.get("info", {}).get("title", "UnnamedAPI")
    base_url = spec.get("servers", [{}])[0].get("url", "")

    endpoints: List[Dict[str, Any]] = []
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, details in methods.items():
            http_method = method.upper()
            if http_method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                continue

            try:
                parameters = details.get("parameters", [])
                resolved_params = []

                for p in parameters:
                    if "$ref" in p:
                        p = resolve_ref(p["$ref"], spec)
                    if p.get("in") in ("query", "path"):
                        resolved_params.append(p["name"])

                if "requestBody" in details:
                    request_body = details["requestBody"]
                    if "$ref" in request_body:
                        request_body = resolve_ref(request_body["$ref"], spec)

                    content = request_body.get("content", {})
                    if "application/json" in content:
                        resolved_params.append("data")

                endpoint = Endpoint(
                    name=normalize_method_name(
                        details.get(
                            "operationId") or f"{http_method}_{path.strip('/').replace('/', '_')}"
                    ),
                    method=http_method,
                    path=path,
                    description=details.get(
                        "summary") or details.get("description", "")
                )
                endpoints.append(asdict(endpoint))

            except Exception as e:
                logger.warning(
                    f"Failed to parse path: {path} method: {method} due to: {e}")

    if save_endpoints:
        logger.info("Saving endpoints to file")

        full_path = f"{save_path.rstrip('/')}/{file_name}"
        logger.info(f"Saving endpoints to {full_path}")

        try:
            with open(full_path, "w") as f:
                if output_format.lower() == "json":
                    json.dump(endpoints, f, indent=2)
                elif output_format.lower() == "yaml":
                    yaml.dump(endpoints, f)
                else:
                    raise ValueError(
                        "Unsupported output format. Choose 'json' or 'yaml'.")
        except Exception as e:
            logger.error(f"Failed to save endpoints to file: {e}")

    return endpoints, {"api_name": api_name, "base_url": base_url or ""}
