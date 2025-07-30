from typing import Any, Optional
import requests

from smartapi.errors import ApiBadGatewayError, ApiBadRequestError, ApiClientError, ApiConflictError, ApiExpectationFailedError, ApiFailedDependencyError, ApiForbiddenError, ApiGatewayTimeoutError, ApiGoneError, ApiHTTPVersionNotSupportedError, ApiInsufficientStorageError, ApiLengthRequiredError, ApiLockedError, ApiLoopDetectedError, ApiMethodNotAllowedError, ApiNetworkAuthRequiredError, ApiNotAcceptableError, ApiNotExtendedError, ApiNotFoundError, ApiNotImplementedError, ApiPayloadTooLargeError, ApiPaymentRequiredError, ApiPreconditionFailedError, ApiPreconditionRequiredError, ApiProxyAuthRequiredError, ApiRangeNotSatisfiableError, ApiRateLimitError, ApiRequestHeaderTooLargeError, ApiServerError, ApiServiceUnavailableError, ApiTeapotError, ApiTimeoutError, ApiTooEarlyError, ApiURITooLongError, ApiUnauthorizedError, ApiUnavailableForLegalReasonsError, ApiUnprocessableEntityError, ApiUnsupportedMediaTypeError, ApiUpgradeRequiredError, ApiVariantAlsoNegotiatesError


def _handle_error_response(
    self,
    response: requests.Response,
    method: str,
    path: str,
    request_id: str
) -> None:
    """Handle error responses with detailed logging."""
    if response.ok:
        return

    try:
        error_data = response.json()
        error_msg = self._extract_error_message(error_data, response)
        error_code = error_data.get("code")
    except ValueError:
        error_msg = response.text or "No error details provided"
        error_code = None

    # Log the error details
    self.logger.error("API error response", extra={
        "method": method,
        "path": path,
        "status_code": response.status_code,
        "error": error_msg,
        "error_code": error_code,
        "request_id": request_id,
        "response_body": error_msg if len(error_msg) < 500 else error_msg[:500] + "...[truncated]"
    })

    exc = self._map_status_to_exception(
        response.status_code,
        f"{method} {path} failed: {error_msg}",
        response
    )

    error_data = None

    if error_code:
        exc.error_code = error_code
    if isinstance(error_data, dict):
        exc.error_details = error_data

    raise exc


def _extract_error_message(self, error_data: Any, response: requests.Response) -> str:
    """Extract error message from error response data."""
    if not isinstance(error_data, dict):
        return str(error_data)

    # Check common error message fields
    for field in ['message', 'error', 'detail', 'description', 'reason']:
        if field in error_data and error_data[field]:
            return str(error_data[field])

    # Check for nested errors
    if 'errors' in error_data:
        if isinstance(error_data['errors'], list):
            return f"Multiple errors: {', '.join(str(e) for e in error_data['errors'])}"
        elif isinstance(error_data['errors'], dict):
            return f"Multiple errors: {str(error_data['errors'])}"

    return response.text or "Unknown error"


def _map_status_to_exception(
    self,
    status_code: int,
    message: str,
    response: Optional[requests.Response] = None
) -> ApiClientError:
    """Map HTTP status code to appropriate exception class."""
    exception_map = {
        400: ApiBadRequestError,
        401: ApiUnauthorizedError,
        402: ApiPaymentRequiredError,
        403: ApiForbiddenError,
        404: ApiNotFoundError,
        405: ApiMethodNotAllowedError,
        406: ApiNotAcceptableError,
        407: ApiProxyAuthRequiredError,
        408: ApiTimeoutError,
        409: ApiConflictError,
        410: ApiGoneError,
        411: ApiLengthRequiredError,
        412: ApiPreconditionFailedError,
        413: ApiPayloadTooLargeError,
        414: ApiURITooLongError,
        415: ApiUnsupportedMediaTypeError,
        416: ApiRangeNotSatisfiableError,
        417: ApiExpectationFailedError,
        418: ApiTeapotError,
        422: ApiUnprocessableEntityError,
        423: ApiLockedError,
        424: ApiFailedDependencyError,
        425: ApiTooEarlyError,
        426: ApiUpgradeRequiredError,
        428: ApiPreconditionRequiredError,
        429: ApiRateLimitError,
        431: ApiRequestHeaderTooLargeError,
        451: ApiUnavailableForLegalReasonsError,
        500: ApiServerError,
        501: ApiNotImplementedError,
        502: ApiBadGatewayError,
        503: ApiServiceUnavailableError,
        504: ApiGatewayTimeoutError,
        505: ApiHTTPVersionNotSupportedError,
        506: ApiVariantAlsoNegotiatesError,
        507: ApiInsufficientStorageError,
        508: ApiLoopDetectedError,
        510: ApiNotExtendedError,
        511: ApiNetworkAuthRequiredError,
    }

    # Special handling for unregistered 5xx errors
    if 500 <= status_code < 600 and status_code not in exception_map:
        return ApiServerError(message, status_code, response)

    exception_class = exception_map.get(status_code, ApiClientError)
    return exception_class(message, status_code, response)


def _map_error_to_exception(
    self,
    error: requests.exceptions.RequestException,
    method: str,
    path: str,
    status_code: Optional[int]
) -> ApiClientError:
    """Map requests exception to our custom exceptions."""
    if isinstance(error, requests.exceptions.Timeout):
        return ApiTimeoutError(f"Request timeout: {method} {path}")
    elif isinstance(error, requests.exceptions.SSLError):
        return ApiClientError(f"SSL error: {str(error)}")
    elif isinstance(error, requests.exceptions.ConnectionError):
        return ApiClientError(f"Connection error: {str(error)}")
    elif isinstance(error, requests.exceptions.TooManyRedirects):
        return ApiClientError(f"Too many redirects: {method} {path}")
    elif isinstance(error, requests.exceptions.URLRequired):
        return ApiClientError(f"Invalid URL: {method} {path}")
    elif isinstance(error, requests.exceptions.MissingSchema):
        return ApiClientError(f"Missing URL schema: {method} {path}")
    elif isinstance(error, requests.exceptions.InvalidSchema):
        return ApiClientError(f"Invalid URL schema: {method} {path}")
    elif isinstance(error, requests.exceptions.InvalidURL):
        return ApiClientError(f"Invalid URL: {method} {path}")
    elif status_code is not None:
        return self._map_status_to_exception(
            status_code,
            f"API request failed: {method} {path} - {str(error)}",
            getattr(error, 'response', None)
        )
    else:
        return ApiClientError(f"Request failed: {method} {path} - {str(error)}")
