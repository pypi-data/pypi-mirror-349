from smartapi.api_client_core import _setup_logging, _configure_session
from smartapi.api_client_requests import _request, _log_request, _execute_request, _process_before_request, _process_after_response
from smartapi.api_client_endpoints import register_endpoints, _create_dynamic_methods, _create_endpoint_method, _generate_method_name
from smartapi.api_client_errors import _handle_error_response, _extract_error_message, _map_status_to_exception, _map_error_to_exception
from smartapi.api_client_response import _process_response, _check_for_business_errors, _handle_mock_response, _create_mock_response
from smartapi.api_client_openapi import from_openapi_spec, _parse_openapi_spec
from smartapi.api_client_postman import from_postman_collection, _parse_postman_collection


def attach_api_client_methods(cls):
    cls._setup_logging = _setup_logging
    cls._configure_session = _configure_session
    cls._request = _request
    cls._log_request = _log_request
    cls._execute_request = _execute_request
    cls._process_before_request = _process_before_request
    cls._process_after_response = _process_after_response
    cls.register_endpoints = register_endpoints
    cls._create_dynamic_methods = _create_dynamic_methods
    cls._create_endpoint_method = _create_endpoint_method
    cls._handle_error_response = _handle_error_response
    cls._extract_error_message = _extract_error_message
    cls._map_status_to_exception = _map_status_to_exception
    cls._map_error_to_exception = _map_error_to_exception
    cls._process_response = _process_response
    cls._check_for_business_errors = _check_for_business_errors
    cls._handle_mock_response = _handle_mock_response
    cls._create_mock_response = _create_mock_response
    cls._generate_method_name = staticmethod(_generate_method_name)
    cls.from_openapi_spec = classmethod(from_openapi_spec)
    cls._parse_openapi_spec = staticmethod(_parse_openapi_spec)
    cls.from_postman_collection = classmethod(from_postman_collection)
    cls._parse_postman_collection = staticmethod(_parse_postman_collection)


class APIClientMixin:
    _setup_logging = staticmethod(_setup_logging)
    _configure_session = staticmethod(_configure_session)
    _request = staticmethod(_request)
    _log_request = staticmethod(_log_request)
    _execute_request = staticmethod(_execute_request)
    _process_before_request = staticmethod(_process_before_request)
    _process_after_response = staticmethod(_process_after_response)
    register_endpoints = staticmethod(register_endpoints)
    _create_dynamic_methods = staticmethod(_create_dynamic_methods)
    _create_endpoint_method = staticmethod(_create_endpoint_method)
    _handle_error_response = staticmethod(_handle_error_response)
    _extract_error_message = staticmethod(_extract_error_message)
    _map_status_to_exception = staticmethod(_map_status_to_exception)
    _map_error_to_exception = staticmethod(_map_error_to_exception)
    _process_response = staticmethod(_process_response)
    _check_for_business_errors = staticmethod(_check_for_business_errors)
    _handle_mock_response = staticmethod(_handle_mock_response)
    _create_mock_response = staticmethod(_create_mock_response)
    _generate_method_name = staticmethod(_generate_method_name)
    from_openapi_spec = classmethod(from_openapi_spec)
    _parse_openapi_spec = staticmethod(_parse_openapi_spec)
    from_postman_collection = classmethod(from_postman_collection)
    _parse_postman_collection = staticmethod(_parse_postman_collection)
