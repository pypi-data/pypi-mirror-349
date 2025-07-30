from typing import Optional
import requests


class ApiClientError(Exception):
    """Base exception for API client errors."""

    def __init__(self, message: str, status_code: Optional[int] = None,
                 response: Optional[requests.Response] = None):
        self.status_code = status_code
        self.response = response
        self.error_code = None
        self.error_details = None
        super().__init__(message)

    def __str__(self):
        base_msg = super().__str__()
        if self.status_code:
            base_msg = f"[{self.status_code}] {base_msg}"
        if self.error_code:
            base_msg = f"{base_msg} (code: {self.error_code})"
        return base_msg


class ApiTimeoutError(ApiClientError):
    """Request timed out."""
    pass


class ApiBadRequestError(ApiClientError):
    """400 Bad Request."""
    pass


class ApiUnauthorizedError(ApiClientError):
    """401 Unauthorized."""
    pass


class ApiPaymentRequiredError(ApiClientError):
    """402 Payment Required."""
    pass


class ApiForbiddenError(ApiClientError):
    """403 Forbidden."""
    pass


class ApiNotFoundError(ApiClientError):
    """404 Not Found."""
    pass


class ApiMethodNotAllowedError(ApiClientError):
    """405 Method Not Allowed."""
    pass


class ApiNotAcceptableError(ApiClientError):
    """406 Not Acceptable."""
    pass


class ApiProxyAuthRequiredError(ApiClientError):
    """407 Proxy Authentication Required."""
    pass


class ApiConflictError(ApiClientError):
    """409 Conflict."""
    pass


class ApiGoneError(ApiClientError):
    """410 Gone."""
    pass


class ApiLengthRequiredError(ApiClientError):
    """411 Length Required."""
    pass


class ApiPreconditionFailedError(ApiClientError):
    """412 Precondition Failed."""
    pass


class ApiPayloadTooLargeError(ApiClientError):
    """413 Payload Too Large."""
    pass


class ApiURITooLongError(ApiClientError):
    """414 URI Too Long."""
    pass


class ApiUnsupportedMediaTypeError(ApiClientError):
    """415 Unsupported Media Type."""
    pass


class ApiRangeNotSatisfiableError(ApiClientError):
    """416 Range Not Satisfiable."""
    pass


class ApiExpectationFailedError(ApiClientError):
    """417 Expectation Failed."""
    pass


class ApiTeapotError(ApiClientError):
    """418 I'm a teapot."""
    pass


class ApiUnprocessableEntityError(ApiClientError):
    """422 Unprocessable Entity."""
    pass


class ApiLockedError(ApiClientError):
    """423 Locked."""
    pass


class ApiFailedDependencyError(ApiClientError):
    """424 Failed Dependency."""
    pass


class ApiTooEarlyError(ApiClientError):
    """425 Too Early."""
    pass


class ApiUpgradeRequiredError(ApiClientError):
    """426 Upgrade Required."""
    pass


class ApiPreconditionRequiredError(ApiClientError):
    """428 Precondition Required."""
    pass


class ApiRateLimitError(ApiClientError):
    """429 Too Many Requests."""

    def __init__(self, message: str, status_code: int, response: requests.Response):
        super().__init__(message, status_code, response)
        self.retry_after = int(response.headers.get('Retry-After', 60))


class ApiRequestHeaderTooLargeError(ApiClientError):
    """431 Request Header Fields Too Large."""
    pass


class ApiUnavailableForLegalReasonsError(ApiClientError):
    """451 Unavailable For Legal Reasons."""
    pass


class ApiServerError(ApiClientError):
    """5xx Server Error."""
    pass


class ApiNotImplementedError(ApiServerError):
    """501 Not Implemented."""
    pass


class ApiBadGatewayError(ApiServerError):
    """502 Bad Gateway."""
    pass


class ApiServiceUnavailableError(ApiServerError):
    """503 Service Unavailable."""
    pass


class ApiGatewayTimeoutError(ApiServerError):
    """504 Gateway Timeout."""
    pass


class ApiHTTPVersionNotSupportedError(ApiServerError):
    """505 HTTP Version Not Supported."""
    pass


class ApiVariantAlsoNegotiatesError(ApiServerError):
    """506 Variant Also Negotiates."""
    pass


class ApiInsufficientStorageError(ApiServerError):
    """507 Insufficient Storage."""
    pass


class ApiLoopDetectedError(ApiServerError):
    """508 Loop Detected."""
    pass


class ApiNotExtendedError(ApiServerError):
    """510 Not Extended."""
    pass


class ApiNetworkAuthRequiredError(ApiServerError):
    """511 Network Authentication Required."""
    pass


class ApiBusinessLogicError(ApiClientError):
    """Business logic error in successful response."""
    pass
