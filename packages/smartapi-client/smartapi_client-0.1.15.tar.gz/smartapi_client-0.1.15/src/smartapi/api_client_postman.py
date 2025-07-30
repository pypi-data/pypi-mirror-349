
# Setup logger
from dataclasses import dataclass, asdict
import logging
import json
import re
from typing import List, Dict, Any, Tuple, Type

import yaml
from smartapi.utils import normalize_method_name


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Endpoint:
    name: str
    method: str
    path: str
    description: str


@classmethod
def from_postman_collection(cls: Type['ApiClient'],
                            collection_path: str,
                            save_endpoints: bool = False,
                            path: str = ".",
                            file_name: str = "endpoints.json",
                            output_format: str = "json",
                            **kwargs) -> 'ApiClient':

    endpoints, metadata = cls._parse_postman_collection(
        collection_path, save_endpoints=save_endpoints,
        save_path=path, file_name=file_name,
        output_format=output_format, **kwargs
    )

    api_name = kwargs.pop("api_name", metadata.get(
        "api_name", "UnnamedCollection"))
    base_url = kwargs.pop("base_url", metadata.get("base_url", ""))

    client = cls(api_name=api_name, base_url=base_url, **kwargs)
    client.register_endpoints(endpoints)
    return client


@staticmethod
def _parse_postman_collection(collection_path: str,
                              save_endpoints: bool = False,
                              save_path: str = ".",
                              file_name: str = "endpoints.json",
                              output_format: str = "json",
                              **kwargs) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:

    try:
        with open(collection_path, 'r') as f:
            collection = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse Postman collection: {e}")

    api_name = collection.get('info', {}).get('name', 'UnnamedCollection')
    base_url = None
    variables = collection.get('variable', [])

    if isinstance(variables, list):
        for var in variables:
            if var.get('key') == 'base_url':
                base_url = var.get('value')

    endpoints: List[Dict[str, Any]] = []

    def resolve_path(path_parts):
        raw = '/' + '/'.join(path_parts)
        return re.sub(r'\{\{(\w+)\}\}', r'{\1}', raw)

    def walk(items):
        if not items:
            return
        for item in items:
            try:
                if 'request' in item:
                    req = item.get('request', {})
                    method = req.get('method', 'GET').upper()
                    url = req.get('url', {})

                    if isinstance(url, dict):
                        path_parts = url.get('path', [])
                        path = resolve_path(path_parts)
                        query_params = [q.get('key') for q in url.get(
                            'query', []) if 'key' in q]
                    else:
                        path = str(url)
                        query_params = []

                    params = list(filter(None, query_params))

                    if "body" in req and req["body"].get("mode") == "raw":
                        params.append("data")

                    endpoint = Endpoint(
                        name=normalize_method_name(
                            item.get("name")) if item.get("name") else "unnamed",
                        method=method,
                        path=path,
                        description=req.get("description", "")
                    )

                    endpoints.append(asdict(endpoint))

                elif 'item' in item:
                    walk(item.get('item', []))

            except Exception as e:
                logger.warning(
                    f"Failed to parse item: {item.get('name')} due to: {e}")

    walk(collection.get('item', []))

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
