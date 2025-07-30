# api_client.py

import logging
import os
import requests
from smartapi.api_client_bindings import attach_api_client_methods
from smartapi.api_client_bindings import APIClientMixin
from smartapi.config import EndpointConfig, HttpMethod, RetryConfig, LogLevel
from typing import Optional, Dict, Any, List, Callable, Union, Tuple, TypeVar, Literal, TypedDict, Type
from typing import TYPE_CHECKING


class ApiClient(APIClientMixin):
    def __init__(
        self,
        api_name: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        default_params: Optional[Dict[str, Any]] = None,
        default_headers: Optional[Dict[str, str]] = None,
        retry_options: Optional[RetryConfig] = None,
        timeout: Union[int, Tuple[int, int]] = 10,
        tracking_id: Optional[str] = None,
        env_prefix: str = "API",
        test_mode: bool = False,
        allowed_methods: Optional[List[HttpMethod]] = None,
        mock_responses: Optional[Dict[str, Any]] = None,
        before_request: Optional[Callable[...,
                                          Optional[Dict[str, Any]]]] = None,
        after_response: Optional[Callable[[
            requests.Response, float], None]] = None,
        debug: bool = False,
        raise_for_status: bool = True,
        log_level: LogLevel = LogLevel.INFO,
        check_business_errors: bool = True,
    ):
        """Initialize the API client with configuration options."""
        self.api_name = api_name
        self.env_prefix = env_prefix.upper()
        self.tracking_id = tracking_id
        self.timeout = timeout
        self.test_mode = test_mode
        self.mock_responses = {
            k: (200, v) if not isinstance(v, tuple) else v
            for k, v in (mock_responses or {}).items()
        }
        self.before_request = before_request
        self.after_response = after_response
        self.debug = debug
        self.raise_for_status = raise_for_status
        self.check_business_errors = check_business_errors
        self.default_params = default_params or {}
        self.default_headers = default_headers or {}
        self.allowed_methods = [m.upper() for m in (
            allowed_methods or ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])]

        # Initialize logging with a structured format
        self.logger = logging.getLogger(f'{api_name}.client')
        self._setup_logging(log_level)

        # Get configuration from environment variables
        self.base_url = base_url or os.getenv(f'{self.env_prefix}_BASE_URL')
        self.api_key = api_key or os.getenv(f'{self.env_prefix}_KEY')

        if not self.base_url:
            raise ValueError(
                f"Base URL not configured. Set {self.env_prefix}_BASE_URL or pass base_url parameter"
            )

        self.session = requests.Session()
        self._configure_session(
            default_params, default_headers, retry_options or {})

        self._api_endpoints: List[EndpointConfig] = []

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()

    def __enter__(self) -> 'ApiClient':
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()

    def __str__(self) -> str:
        """String representation of the client."""
        return (
            f"{self.api_name}ApiClient("
            f"endpoints={len(self._api_endpoints)}, "
            f"base_url={self.base_url}, "
            f"test_mode={self.test_mode})"
        )

    def version(self) -> str:
        """Get the version of the API client."""
        return "1.0.0"


# Attach methods
attach_api_client_methods(ApiClient)
