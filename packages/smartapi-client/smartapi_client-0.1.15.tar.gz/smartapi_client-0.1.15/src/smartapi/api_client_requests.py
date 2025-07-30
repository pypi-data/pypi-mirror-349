import os
import time
import requests
from typing import Optional, Dict, Any, List, Callable, Union, Tuple, TypeVar, Literal, TypedDict, Type
from dataclasses import dataclass

from smartapi.errors import ApiClientError, ApiMethodNotAllowedError

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


@dataclass
class ApiResponse:
    status_code: int
    data: Optional[JsonType] = None
    headers: Optional[Dict[str, str]] = None
    elapsed: Optional[float] = None
    raw_response: Optional[requests.Response] = None


def _request(
    self,
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], str, bytes]] = None,
    headers: Optional[Dict[str, str]] = None,
    return_raw_response: bool = False,
    return_api_response: bool = False,
) -> Union[Dict[str, Any], ApiResponse, requests.Response]:
    """Execute an API request with comprehensive error handling."""
    method = method.upper()
    if method not in self.allowed_methods:
        raise ApiMethodNotAllowedError(
            f"Method {method} is not allowed. Allowed methods: {self.allowed_methods}"
        )

    request_start = time.time()
    response = None
    request_id = f"{int(time.time() * 1000)}-{os.urandom(2).hex()}"

    try:
        merged_params = {**self.default_params, **(params or {})}
        url = f"{self.base_url}{path}"
        merged_headers = {**self.default_headers, **(headers or {})}
        mock_key = f"{method} {path}"

        # Add request ID to headers
        merged_headers['X-Request-ID'] = request_id

        if self.test_mode and mock_key in self.mock_responses:
            self.logger.info("Mock response", extra={
                "method": method,
                "path": path,
                "request_id": request_id,
                "mock": True
            })
            return self._handle_mock_response(
                mock_key, return_raw_response, return_api_response
            )

        # Process before_request hook
        merged_params, merged_headers, data = self._process_before_request(
            method, url, merged_params, merged_headers, data
        )

        self._log_request(method, path, request_id,
                          merged_params, merged_headers, data)

        try:
            response = self._execute_request(
                method, url, merged_params, data, merged_headers
            )
            duration = round(time.time() - request_start, 2)

            self.logger.info("Request completed", extra={
                "method": method,
                "path": path,
                "status_code": response.status_code,
                "duration": duration,
                "request_id": request_id
            })

            # Process after_response hook
            self._process_after_response(response, duration)

            # Handle error responses
            if self.raise_for_status:
                self._handle_error_response(
                    response, method, path, request_id)

            # Process and return the response
            return self._process_response(
                response, duration, return_raw_response, return_api_response, request_id
            )

        except requests.exceptions.RequestException as e:
            status_code = getattr(
                getattr(e, 'response', None), 'status_code', None)
            self.logger.error("Request failed", extra={
                "method": method,
                "path": path,
                "error": str(e),
                "status_code": status_code,
                "request_id": request_id,
                "exc_info": not isinstance(e, (requests.exceptions.Timeout,
                                               requests.exceptions.ConnectionError))
            })
            raise self._map_error_to_exception(
                e, method, path, status_code
            ) from None  # from None to avoid chained exceptions in logs

    except Exception as e:
        if not isinstance(e, ApiClientError):
            self.logger.error("Unexpected error in API request", extra={
                "method": method,
                "path": path,
                "error": str(e),
                "request_id": request_id,
                "exc_info": True
            })
            raise ApiClientError(f"Unexpected error: {str(e)}") from None
        raise


def _log_request(
    self,
    method: str,
    path: str,
    request_id: str,
    params: Dict[str, Any],
    headers: Dict[str, str],
    data: Optional[Union[Dict[str, Any], str, bytes]]
) -> None:
    """Log request details in a structured way."""
    log_data = {
        "method": method,
        "path": path,
        "request_id": request_id,
        "params": params,
    }

    # Redact sensitive headers
    redacted_headers = {
        k: "*****" if k.lower() in ['authorization', 'api-key'] else v
        for k, v in headers.items()
    }
    log_data["headers"] = redacted_headers

    if self.debug:
        try:
            if isinstance(data, (str, bytes)):
                log_data["body"] = str(data)[:500]
            else:
                log_data["body"] = data
        except Exception:
            log_data["body"] = "<unserializable data>"

        self.logger.debug("Request details", extra=log_data)


def _execute_request(
    self,
    method: str,
    url: str,
    params: Dict[str, Any],
    data: Optional[Union[Dict[str, Any], str, bytes]],
    headers: Dict[str, str]
) -> requests.Response:
    """Execute the HTTP request with retry logic."""
    files = None
    json_data = None
    form_data = None

    content_type = headers.get('Content-Type', '').lower()

    if content_type == 'application/json' or isinstance(data, dict):
        json_data = data if isinstance(data, dict) else None
    elif content_type == 'application/x-www-form-urlencoded':
        form_data = data if isinstance(data, dict) else None
    elif content_type.startswith('multipart/form-data') and isinstance(data, dict):
        # Split out files from regular fields
        files = {}
        form_data = {}
        for k, v in data.items():
            if hasattr(v, 'read'):
                files[k] = v
            else:
                form_data[k] = v
    elif isinstance(data, (str, bytes)):
        # For raw body content like XML, plain text, etc.
        return self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=self.timeout
        )

    return self.session.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        timeout=self.timeout,
        json=json_data,
        data=form_data,
        files=files
    )


def _process_before_request(
    self,
    method: str,
    url: str,
    params: Dict[str, Any],
    headers: Dict[str, str],
    data: Optional[Union[Dict[str, Any], str, bytes]]
) -> Tuple[Dict[str, Any], Dict[str, str], Optional[Union[Dict[str, Any], str, bytes]]]:
    """Process before_request hook if provided."""
    if self.before_request:
        hook_result = self.before_request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers
        )
        if isinstance(hook_result, dict):
            params.update(hook_result.get("params", {}))
            headers.update(hook_result.get("headers", {}))
            if "data" in hook_result:
                data = hook_result["data"]
    return params, headers, data


def _process_after_response(self, response: requests.Response, duration: float) -> None:
    """Process after_response hook if provided."""
    if self.after_response:
        self.after_response(response=response, duration=duration)
