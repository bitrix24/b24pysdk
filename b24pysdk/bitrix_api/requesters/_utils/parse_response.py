from typing import Dict, Text, Type

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from ....error import (
    BitrixAPIAccessDenied,
    BitrixAPIAllowedOnlyIntranetUser,
    BitrixAPIAuthorizationError,
    BitrixAPIBadRequest,
    BitrixAPIError,
    BitrixAPIErrorBatchLengthExceeded,
    BitrixAPIErrorBatchMethodNotAllowed,
    BitrixAPIErrorManifestIsNotAvailable,
    BitrixAPIErrorOAuth,
    BitrixAPIErrorUnexpectedAnswer,
    BitrixAPIExpiredToken,
    BitrixAPIForbidden,
    BitrixAPIInsufficientScope,
    BitrixAPIInternalServerError,
    BitrixAPIInvalidArgValue,
    BitrixAPIInvalidCredentials,
    BitrixAPIInvalidRequest,
    BitrixAPIMethodConfirmDenied,
    BitrixAPIMethodConfirmWaiting,
    BitrixAPIMethodNotAllowed,
    BitrixAPINoAuthFound,
    BitrixAPINotFound,
    BitrixAPIOverloadLimit,
    BitrixAPIQueryLimitExceeded,
    BitrixAPIServiceUnavailable,
    BitrixAPIUnauthorized,
    BitrixAPIUserAccessError,
    BitrixAPIWrongAuthType,
    BitrixOAuthInvalidClient,
    BitrixOAuthInvalidGrant,
    BitrixOAuthInvalidScope,
    BitrixOauthWrongClient,
    BitrixResponse302JSONDecodeError,
    BitrixResponse403JSONDecodeError,
    BitrixResponse500JSONDecodeError,
    BitrixResponseJSONDecodeError,
)
from ....utils.types import JSONDict

_EXCEPTIONS_BY_ERROR: Dict[Text, Type[BitrixAPIError]] = {
    # 200
    "WRONG_CLIENT": BitrixOauthWrongClient,
    # 400
    "ERROR_BATCH_LENGTH_EXCEEDED": BitrixAPIErrorBatchLengthExceeded,
    "INVALID_ARG_VALUE": BitrixAPIInvalidArgValue,
    "INVALID_CLIENT": BitrixOAuthInvalidClient,
    "INVALID_GRANT": BitrixOAuthInvalidGrant,
    "INVALID_REQUEST": BitrixAPIInvalidRequest,
    # 401
    "AUTHORIZATION_ERROR": BitrixAPIAuthorizationError,
    "ERROR_OAUTH": BitrixAPIErrorOAuth,
    "EXPIRED_TOKEN": BitrixAPIExpiredToken,
    "METHOD_CONFIRM_WAITING": BitrixAPIMethodConfirmWaiting,
    "NO_AUTH_FOUND": BitrixAPINoAuthFound,
    # 403
    "ACCESS_DENIED": BitrixAPIAccessDenied,
    "ALLOWED_ONLY_INTRANET_USER": BitrixAPIAllowedOnlyIntranetUser,
    "INSUFFICIENT_SCOPE": BitrixAPIInsufficientScope,
    "INVALID_CREDENTIALS": BitrixAPIInvalidCredentials,
    "METHOD_CONFIRM_DENIED": BitrixAPIMethodConfirmDenied,
    "USER_ACCESS_ERROR": BitrixAPIUserAccessError,
    "WRONG_AUTH_TYPE": BitrixAPIWrongAuthType,
    "INVALID_SCOPE": BitrixOAuthInvalidScope,
    # 404
    "NOT_FOUND": BitrixAPINotFound,
    "ERROR_MANIFEST_IS_NOT_AVAILABLE": BitrixAPIErrorManifestIsNotAvailable,
    # 405
    "ERROR_BATCH_METHOD_NOT_ALLOWED": BitrixAPIErrorBatchMethodNotAllowed,
    # 500
    "ERROR_UNEXPECTED_ANSWER": BitrixAPIErrorUnexpectedAnswer,
    "INTERNAL_SERVER_ERROR": BitrixAPIInternalServerError,
    # 503
    "OVERLOAD_LIMIT": BitrixAPIOverloadLimit,
    "QUERY_LIMIT_EXCEEDED": BitrixAPIQueryLimitExceeded,
}
""""""

_EXCEPTIONS_BY_STATUS_CODE: Dict[int, Type[BitrixAPIError]] = {
    400: BitrixAPIBadRequest,
    401: BitrixAPIUnauthorized,
    403: BitrixAPIForbidden,
    404: BitrixAPINotFound,
    405: BitrixAPIMethodNotAllowed,
    500: BitrixAPIInternalServerError,
    503: BitrixAPIServiceUnavailable,
}
""""""

_EXCEPTIONS_BY_JSON_DECODE_RESPONSE_STATUS_CODE: Dict[int, Type[BitrixResponseJSONDecodeError]] = {
    302: BitrixResponse302JSONDecodeError,
    403: BitrixResponse403JSONDecodeError,
    500: BitrixResponse500JSONDecodeError,
}


def _raise_http_error(response: requests.Response):
    raise HTTPError(
        f"{response.status_code} Client Error: {response.json()['error']} for url: {response.url}",
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
                or BitrixResponseJSONDecodeError
        )
        raise exception_class(original_error=error, response=response) from error

    try:
        response.raise_for_status()

        if "error" in json_response:
            _raise_http_error(response)

    except HTTPError as error:
        exception_class = (
                _EXCEPTIONS_BY_ERROR.get(str(json_response.get("error", "")).upper()) or
                _EXCEPTIONS_BY_STATUS_CODE.get(response.status_code) or
                BitrixAPIError
        )
        raise exception_class(json_response=json_response, response=response) from error

    else:
        return json_response
