"""
Utilities for parsing Bitrix API responses.

This module converts raw `requests.Response` objects into Python dictionaries
and raises appropriate SDK exceptions when the response indicates an error.

Both legacy Bitrix REST API error formats and the newer Bitrix REST API v3
error format are supported.
"""

from typing import Dict, Text, Type

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from .... import errors
from ....errors import oauth as errors_oauth
from ....errors import v3 as errors_v3
from ....utils.types import JSONDict

__all__ = [
    "parse_response",
]

_EXCEPTIONS_BY_JSON_DECODE_RESPONSE_STATUS_CODE: Dict[int, Type[errors.BitrixResponseJSONDecodeError]] = {
    302: errors.BitrixResponse302JSONDecodeError,
    403: errors.BitrixResponse403JSONDecodeError,
    500: errors.BitrixResponse500JSONDecodeError,
}
"""
Mapping of HTTP status codes to specialized JSON decode exceptions.

These exceptions are raised when the server response cannot be parsed as JSON.
Certain HTTP statuses are mapped to more specific exception classes to provide
better diagnostics.
"""

_EXCEPTIONS_BY_STATUS_CODE: Dict[int, Type[errors.BitrixAPIError]] = {
    400: errors.BitrixAPIBadRequest,
    401: errors.BitrixAPIUnauthorized,
    403: errors.BitrixAPIForbidden,
    404: errors.BitrixAPINotFound,
    405: errors.BitrixAPIMethodNotAllowed,
    410: errors.BitrixAPIGone,
    429: errors.BitrixAPITooManyRequests,
    500: errors.BitrixAPIInternalServerError,
    503: errors.BitrixAPIServiceUnavailable,
}
"""
Mapping of HTTP status codes to Bitrix API exception classes.

Used when the API returns an error response without a recognizable
application-level error code.
"""

_EXCEPTIONS_V3_BY_STATUS_CODE: Dict[int, Type[errors_v3.BitrixAPIError]] = {
    400: errors_v3.BitrixAPIBadRequest,
    401: errors_v3.BitrixAPIUnauthorized,
}
"""
Mapping of HTTP status codes to Bitrix REST API v3 exception classes.

Used when the response contains a structured error payload but the
specific error code is not recognized.
"""

_EXCEPTIONS_BY_ERROR: Dict[Text, Type[errors.BitrixAPIError]] = {
    # 200
    "WRONG_CLIENT": errors_oauth.BitrixOauthWrongClient,
    # 400
    "INVALID_ARG_VALUE": errors.BitrixAPIInvalidArgValue,
    "INVALID_CLIENT": errors_oauth.BitrixOAuthInvalidClient,
    "INVALID_GRANT": errors_oauth.BitrixOAuthInvalidGrant,
    "INVALID_REQUEST": errors.BitrixAPIInvalidRequest,
    # 401
    "AUTHORIZATION_ERROR": errors.BitrixAPIAuthorizationError,
    "APPLICATION_NOT_FOUND": errors.BitrixAPIApplicationNotFound,
    "ERROR_OAUTH": errors.BitrixAPIErrorOAuth,
    "EXPIRED_TOKEN": errors.BitrixAPIExpiredToken,
    "METHOD_CONFIRM_WAITING": errors.BitrixAPIMethodConfirmWaiting,
    "NO_AUTH_FOUND": errors.BitrixAPINoAuthFound,
    "NOT_INSTALLED": errors_oauth.BitrixOAuthNotInstalled,
    "INVALID_TOKEN": errors.BitrixAPIInvalidToken,
    "PAYMENT_REQUIRED": errors.BitrixAPIPaymentRequired,
    # 403
    "ACCESS_DENIED": errors.BitrixAPIAccessDenied,
    "ALLOWED_ONLY_INTRANET_USER": errors.BitrixAPIAllowedOnlyIntranetUser,
    "INSUFFICIENT_SCOPE": errors.BitrixAPIInsufficientScope,
    "INVALID_CREDENTIALS": errors.BitrixAPIInvalidCredentials,
    "METHOD_CONFIRM_DENIED": errors.BitrixAPIMethodConfirmDenied,
    "USER_ACCESS_ERROR": errors.BitrixAPIUserAccessError,
    "WRONG_AUTH_TYPE": errors.BitrixAPIWrongAuthType,
    "INVALID_SCOPE": errors_oauth.BitrixOAuthInvalidScope,
    # 404
    "NOT_FOUND": errors.BitrixAPINotFound,
    # 410
    "PORTAL_DELETED": errors.BitrixAPIPortalDeleted,
    # 429
    "OPERATION_TIME_LIMIT": errors.BitrixAPIOperationTimeLimit,
    # 500
    "ERROR_UNEXPECTED_ANSWER": errors.BitrixAPIErrorUnexpectedAnswer,
    "INTERNAL_SERVER_ERROR": errors.BitrixAPIInternalServerError,
    # 503
    "OVERLOAD_LIMIT": errors.BitrixAPIOverloadLimit,
    "QUERY_LIMIT_EXCEEDED": errors.BitrixAPIQueryLimitExceeded,
}
"""
Mapping of Bitrix API error codes to exception classes.

The key corresponds to the `error` field returned by the API.
These mappings allow the SDK to raise precise exception types
based on the server-reported error identifier.
"""

_EXCEPTIONS_V3_BY_CODE: Dict[Text, Type[errors_v3.BitrixAPIError]] = {
    "BITRIX_REST_V3_EXCEPTION_ACCESSDENIEDEXCEPTION": errors_v3.BitrixAPIAccessDeniedException,
    "BITRIX_REST_V3_EXCEPTION_ENTITYNOTFOUNDEXCEPTION": errors_v3.BitrixAPIEntityNotFoundException,
    "BITRIX_REST_V3_EXCEPTION_VALIDATION_REQUESTVALIDATIONEXCEPTION": errors_v3.BitrixAPIValidationRequestValidationException,
    "BITRIX_REST_V3_EXCEPTION_INVALIDFILTEREXCEPTION": errors_v3.BitrixAPIInvalidFilterException,
    "BITRIX_REST_V3_EXCEPTION_INVALIDPAGINATIONEXCEPTION": errors_v3.BitrixAPIInvalidPaginationException,
    "BITRIX_REST_V3_EXCEPTION_UNKNOWNDTOPROPERTYEXCEPTION": errors_v3.BitrixAPIUnknownDTOPropertyException,
    "BITRIX_REST_V3_EXCEPTION_VALIDATION_DTOVALIDATIONEXCEPTION": errors_v3.BitrixAPIValidationDTOValidationException,
}
"""
Mapping of Bitrix REST API v3 error codes to exception classes.

In API v3 the error payload contains a structured object with a
`code` field. This mapping translates that code into the appropriate
SDK exception class.
"""


def _raise_http_error(response: requests.Response):
    """
    Raise a `requests.HTTPError` based on the API error payload.

    This helper extracts the error identifier from the response JSON
    and raises a standard `HTTPError` which will later be translated
    into a more specific SDK exception.

    Parameters
    ----------
    response : requests.Response
        HTTP response returned by the API.
    """

    error_payload = response.json()["error"]
    error = error_payload.get("code") if isinstance(error_payload, dict) else error_payload

    raise HTTPError(
        f"{response.status_code} Client Error: {error} for url: {response.url}",
        response=response,
    )


def parse_response(response: requests.Response) -> JSONDict:
    """
    Parse a Bitrix API HTTP response.

    This function converts the raw HTTP response into a Python dictionary
    and raises appropriate SDK exceptions when the response indicates
    an error condition.

    The parser supports both legacy Bitrix REST API error formats and
    the newer Bitrix REST API v3 structured error format.

    Error handling flow
    -------------------
    1. Attempt to parse the response body as JSON.
    2. If JSON parsing fails, raise `BitrixResponseJSONDecodeError`
       or a more specific subclass depending on the HTTP status code.
    3. If the HTTP response indicates an error or the JSON payload
       contains an `error` field, determine the appropriate SDK
       exception class and raise it.

    Parameters
    ----------
    response : requests.Response
        HTTP response returned by the Bitrix API.

    Returns
    -------
    JSONDict
        Parsed JSON response body.

    Raises
    ------
    BitrixAPIError
        Base class for all API-level errors raised by the SDK.
        More specific subclasses may be raised depending on the
        error code or HTTP status.

    BitrixResponseJSONDecodeError
        Raised when the response body cannot be parsed as JSON.
    """

    try:
        json_response = response.json()
    except JSONDecodeError as error:
        exception_class = (
                _EXCEPTIONS_BY_JSON_DECODE_RESPONSE_STATUS_CODE.get(response.status_code)
                or errors.BitrixResponseJSONDecodeError
        )
        raise exception_class(response=response) from error

    try:
        response.raise_for_status()

        if "error" in json_response:
            _raise_http_error(response)

    except HTTPError as error:
        error_payload = json_response.get("error")

        if isinstance(error_payload, dict):
            error_code = error_payload.get("code")
            exception_class = (
                    _EXCEPTIONS_V3_BY_CODE.get(str(error_code or "").upper())
                    or _EXCEPTIONS_V3_BY_STATUS_CODE.get(response.status_code)
                    or errors_v3.BitrixAPIError
            )
            raise exception_class(json_response=json_response, response=response) from error

        exception_class = (
                _EXCEPTIONS_BY_ERROR.get(str(error_payload or "").upper()) or
                _EXCEPTIONS_BY_STATUS_CODE.get(response.status_code) or
                errors.BitrixAPIError
        )
        raise exception_class(json_response=json_response, response=response) from error

    else:
        return json_response
