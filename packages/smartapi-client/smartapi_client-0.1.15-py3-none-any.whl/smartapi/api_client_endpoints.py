import inspect
from typing import Any, Callable, Dict, List, Optional, Union
import requests

from smartapi.api_client_requests import ApiResponse
from smartapi.config import EndpointConfig, HttpMethod


def register_endpoints(self, endpoints: List[EndpointConfig]) -> None:
    """Register API endpoints and create dynamic methods for them."""
    self._api_endpoints = endpoints
    self._create_dynamic_methods()


def _create_dynamic_methods(self) -> None:
    """Create dynamic methods for registered endpoints."""
    for endpoint in self._api_endpoints:
        method_name = endpoint.get("name") or self._generate_method_name(
            endpoint["method"], endpoint["path"]
        )
        endpoint_method = self._create_endpoint_method(
            endpoint["method"],
            endpoint["path"],
            endpoint.get("params", []),
            endpoint.get("description")
        )
        setattr(self, method_name, endpoint_method)
        self.logger.debug(f"Created endpoint method: {method_name}")


def _create_endpoint_method(
    self,
    http_method: HttpMethod,
    path: str,
    params: List[str],
    description: Optional[str] = None
) -> Callable[..., Union[Dict[str, Any], ApiResponse, requests.Response]]:
    """Create a method for a specific endpoint."""
    def endpoint_method(**kwargs) -> Union[Dict[str, Any], ApiResponse, requests.Response]:
        """{description}

        Args:
            {params_doc}
            return_raw_response: If True, returns the raw requests.Response
            return_api_response: If True, returns an ApiResponse object

        Returns:
            Response data as dict, or ApiResponse/Response object based on flags
        """
        path_params = {}
        query_params = {}
        request_data = None
        headers = kwargs.get("headers", {})

        for param in params:
            if param in kwargs:
                if f"{{{param}}}" in path:
                    path_params[param] = kwargs[param]
                else:
                    query_params[param] = kwargs[param]

        request_data = kwargs.get("data", kwargs.get("body"))
        return_raw_response = kwargs.get("return_raw_response", False)
        return_api_response = kwargs.get("return_api_response", False)

        formatted_path = path.format(**path_params)

        return self._request(
            method=http_method,
            path=formatted_path,
            params=query_params,
            data=request_data,
            headers=headers,
            return_raw_response=return_raw_response,
            return_api_response=return_api_response,
        )

    # Generate proper docstring
    params_doc = "\n                ".join(
        f"{param}: Value for {param} parameter"
        for param in params
    )

    # Reserved param names (already added manually below)
    reserved_names = {"data", "headers",
                      "return_raw_response", "return_api_response"}

    # Filter out reserved param names for signature and docstring
    filtered_params = [p for p in params if p not in reserved_names]

    # Create docstring
    params_doc = "\n                ".join(
        f"{param}: Value for {param} parameter" for param in filtered_params
    )
    endpoint_method.__doc__ = endpoint_method.__doc__.format(
        description=description or f"{http_method} {path} endpoint",
        params_doc=params_doc
    )

    # Add signature for better IDE support
    sig = inspect.signature(endpoint_method)
    signature_params = [
        inspect.Parameter(
            name=param,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Any
        ) for param in filtered_params
    ] + [
        inspect.Parameter(
            name="data",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Optional[Union[Dict[str, Any], str]],
            default=None
        ),
        inspect.Parameter(
            name="headers",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Optional[Dict[str, str]],
            default=None
        ),
        inspect.Parameter(
            name="return_raw_response",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=bool,
            default=False
        ),
        inspect.Parameter(
            name="return_api_response",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=bool,
            default=False
        )
    ]
    endpoint_method.__signature__ = sig.replace(
        parameters=signature_params)

    return endpoint_method


@staticmethod
def _generate_method_name(http_method: str, path: str) -> str:
    """Generate a method name from HTTP method and path."""
    clean_path = path.lower().strip("/").split("{")[0]
    clean_path = ''.join(c if c.isalnum() else '_' for c in clean_path)
    method_prefix = {
        "GET": "get",
        "POST": "create",
        "PUT": "update",
        "PATCH": "modify",
        "DELETE": "delete",
        "HEAD": "head",
        "OPTIONS": "options",
    }.get(http_method.upper(), http_method.lower())
    clean_path = '_'.join(filter(None, clean_path.split('_')))
    return f"{method_prefix}_{clean_path}"
