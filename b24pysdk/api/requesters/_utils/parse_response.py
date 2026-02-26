from typing import Dict, Text, Type

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from .... import error as errors
from ....error import v3 as errors_v3
from ....utils.types import JSONDict

__all__ = [
    "parse_response",
]

_EXCEPTIONS_BY_ERROR: Dict[Text, Type[errors.BitrixAPIError]] = {
    # 200
    "WRONG_CLIENT": errors.BitrixOauthWrongClient,
    # 400
    "INVALID_ARG_VALUE": errors.BitrixAPIInvalidArgValue,
    "INVALID_CLIENT": errors.BitrixOAuthInvalidClient,
    "INVALID_GRANT": errors.BitrixOAuthInvalidGrant,
    "INVALID_REQUEST": errors.BitrixAPIInvalidRequest,
    # 401
    "AUTHORIZATION_ERROR": errors.BitrixAPIAuthorizationError,
    "ERROR_OAUTH": errors.BitrixAPIErrorOAuth,
    "EXPIRED_TOKEN": errors.BitrixAPIExpiredToken,
    "METHOD_CONFIRM_WAITING": errors.BitrixAPIMethodConfirmWaiting,
    "NO_AUTH_FOUND": errors.BitrixAPINoAuthFound,
    "INVALID_TOKEN": errors.BitrixAPIInvalidToken,
    # 403
    "ACCESS_DENIED": errors.BitrixAPIAccessDenied,
    "ALLOWED_ONLY_INTRANET_USER": errors.BitrixAPIAllowedOnlyIntranetUser,
    "INSUFFICIENT_SCOPE": errors.BitrixAPIInsufficientScope,
    "INVALID_CREDENTIALS": errors.BitrixAPIInvalidCredentials,
    "METHOD_CONFIRM_DENIED": errors.BitrixAPIMethodConfirmDenied,
    "USER_ACCESS_ERROR": errors.BitrixAPIUserAccessError,
    "WRONG_AUTH_TYPE": errors.BitrixAPIWrongAuthType,
    "INVALID_SCOPE": errors.BitrixOAuthInvalidScope,
    # 404
    "NOT_FOUND": errors.BitrixAPINotFound,
    # 429
    "OPERATION_TIME_LIMIT": errors.BitrixAPIOperationTimeLimit,
    # 500
    "ERROR_UNEXPECTED_ANSWER": errors.BitrixAPIErrorUnexpectedAnswer,
    "INTERNAL_SERVER_ERROR": errors.BitrixAPIInternalServerError,
    # 503
    "OVERLOAD_LIMIT": errors.BitrixAPIOverloadLimit,
    "QUERY_LIMIT_EXCEEDED": errors.BitrixAPIQueryLimitExceeded,
}
""""""

_EXCEPTIONS_BY_V3_CODE: Dict[Text, Type[errors_v3.BitrixAPIError]] = {
    "BITRIX_REST_V3_EXCEPTION_ACCESSDENIEDEXCEPTION": errors_v3.BitrixAPIAccessDeniedException,
    "BITRIX_REST_V3_EXCEPTION_ENTITYNOTFOUNDEXCEPTION": errors_v3.BitrixAPIEntityNotFoundException,
    "BITRIX_REST_V3_EXCEPTION_VALIDATION_REQUESTVALIDATIONEXCEPTION": errors_v3.BitrixAPIValidationRequestValidationException,
    "BITRIX_REST_V3_EXCEPTION_INVALIDFILTEREXCEPTION": errors_v3.BitrixAPIInvalidFilterException,
    "BITRIX_REST_V3_EXCEPTION_INVALIDPAGINATIONEXCEPTION": errors_v3.BitrixAPIInvalidPaginationException,
    "BITRIX_REST_V3_EXCEPTION_UNKNOWNDTOPROPERTYEXCEPTION": errors_v3.BitrixAPIUnknownDTOPropertyException,
    "BITRIX_REST_V3_EXCEPTION_VALIDATION_DTOVALIDATIONEXCEPTION": errors_v3.BitrixAPIValidationDTOValidationException,
}
""""""

_EXCEPTIONS_BY_V3_STATUS_CODE: Dict[int, Type[errors_v3.BitrixAPIError]] = {
    400: errors_v3.BitrixAPIBadRequest,
    401: errors_v3.BitrixAPIUnauthorized,
}
""""""

_EXCEPTIONS_BY_STATUS_CODE: Dict[int, Type[errors.BitrixAPIError]] = {
    400: errors.BitrixAPIBadRequest,
    401: errors.BitrixAPIUnauthorized,
    403: errors.BitrixAPIForbidden,
    404: errors.BitrixAPINotFound,
    405: errors.BitrixAPIMethodNotAllowed,
    429: errors.BitrixAPITooManyRequests,
    500: errors.BitrixAPIInternalServerError,
    503: errors.BitrixAPIServiceUnavailable,
}
""""""

_EXCEPTIONS_BY_JSON_DECODE_RESPONSE_STATUS_CODE: Dict[int, Type[errors.BitrixResponseJSONDecodeError]] = {
    302: errors.BitrixResponse302JSONDecodeError,
    403: errors.BitrixResponse403JSONDecodeError,
    500: errors.BitrixResponse500JSONDecodeError,
}


def _raise_http_error(response: requests.Response):
    error_payload = response.json()["error"]
    error = error_payload.get("code") if isinstance(error_payload, dict) else error_payload

    raise HTTPError(
        f"{response.status_code} Client Error: {error} for url: {response.url}",
        response=response,
    )


def parse_response(response: requests.Response) -> JSONDict:
    """
    Parses the responses from the API server. If responses body contains an error message, raises appropriate exception

    Args:
        response: responses returned by the API server

    Returns:
        dictionary containing the parsed responses of the API server

    Raises:
        BitrixAPIError: base class for all API-related errors. Depening on an error code and/or an HTTP status code, more specific exception subclassed from BitrixAPIError will be raised.
                        These exceptions indicate that the API server successfully processed the responses, but some occured during API method execution.
        BitrixResponseJSONDecodeError: if responses returned by the API server is not a valid JSON
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
                    _EXCEPTIONS_BY_V3_CODE.get(str(error_code or "").upper())
                    or _EXCEPTIONS_BY_V3_STATUS_CODE.get(response.status_code)
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
