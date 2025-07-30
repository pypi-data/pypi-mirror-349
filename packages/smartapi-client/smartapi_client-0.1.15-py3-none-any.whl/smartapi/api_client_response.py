import json
from typing import Any, Dict, Union
import requests
from smartapi.api_client_requests import ApiResponse
from smartapi.errors import ApiBusinessLogicError


def _process_response(
    self,
    response: requests.Response,
    duration: float,
    return_raw: bool,
    return_api: bool,
    request_id: str
) -> Union[Dict[str, Any], ApiResponse, requests.Response]:
    """Process the response based on return format flags."""
    if return_raw:
        return response

    try:
        response_data = response.json()

        if self.debug:
            self.logger.debug("Response data", extra={
                "request_id": request_id,
                "data": response_data
            })

        if self.check_business_errors:
            self._check_for_business_errors(response_data, request_id)

        if return_api:
            return ApiResponse(
                status_code=response.status_code,
                data=response_data,
                headers=dict(response.headers),
                elapsed=duration,
                raw_response=response
            )
        return response_data
    except ValueError:
        if return_api:
            return ApiResponse(
                status_code=response.status_code,
                data=response.text,
                headers=dict(response.headers),
                elapsed=duration,
                raw_response=response
            )
        return {"raw_text": response.text, "status_code": response.status_code}


def _check_for_business_errors(self, response_data: Dict[str, Any], request_id: str) -> None:
    """Check for business logic errors in successful responses."""
    if isinstance(response_data, dict):
        if 'success' in response_data and not response_data['success']:
            error_msg = response_data.get(
                'error', 'Unknown business error')
            self.logger.error("Business logic error", extra={
                "request_id": request_id,
                "error": error_msg,
                "response_data": response_data
            })
            raise ApiBusinessLogicError(error_msg)
        if 'error' in response_data and response_data['error']:
            self.logger.error("Business logic error", extra={
                "request_id": request_id,
                "error": response_data['error'],
                "response_data": response_data
            })
            raise ApiBusinessLogicError(response_data['error'])


# def _handle_mock_response(
#     self,
#     mock_key: str,
#     return_raw: bool,
#     return_api: bool
# ) -> Union[Dict[str, Any], ApiResponse, requests.Response]:
#     """Handle mock response based on return format flags."""
#     mock_response = self.mock_responses[mock_key]
#     if return_raw:
#         return self._create_mock_response(mock_response)
#     if return_api:
#         return ApiResponse(
#             status_code=200,
#             data=mock_response,
#             raw_response=self._create_mock_response(mock_response)
#         )
#     return mock_response


# def _create_mock_response(self, data: Any) -> requests.Response:
#     """Create a mock response object for testing."""
#     response = requests.Response()
#     response.status_code = 200
#     response._content = json.dumps(data).encode(
#     ) if not isinstance(data, (str, bytes)) else data
#     return response

def _handle_mock_response(self, mock_key, return_raw, return_api):
    mock_data = self.mock_responses[mock_key]
    status_code = 200
    data = mock_data
    if isinstance(mock_data, tuple) and len(mock_data) == 2:
        status_code, data = mock_data

    if return_raw:
        return self._create_mock_response(data, status_code)
    if return_api:
        return ApiResponse(
            status_code=status_code,
            data=data,
            raw_response=self._create_mock_response(data, status_code)
        )
    return data

# Updated _create_mock_response


def _create_mock_response(self, data: Any, status_code: int = 200) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(data).encode(
    ) if not isinstance(data, (str, bytes)) else data
    return response
