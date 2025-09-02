from typing import Dict, Text, Type

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from ...error import (
    BitrixAPIAccessDenied,
    BitrixAPIAllowedOnlyIntranetUser,
    BitrixAPIBadRequest,
    BitrixAPIError,
    BitrixAPIErrorBatchLengthExceeded,
    BitrixAPIErrorBatchMethodNotAllowed,
    BitrixAPIErrorManifestIsNotAvailable,
    BitrixAPIErrorUnexpectedAnswer,
    BitrixAPIExpiredToken,
    BitrixAPIForbidden,
    BitrixAPIInsufficientScope,
    BitrixAPIInternalServerError,
    BitrixAPIInvalidArgValue,
    BitrixAPIInvalidCredentials,
    BitrixAPIInvalidRequest,
    BitrixAPIMethodNotAllowed,
    BitrixAPINoAuthFound,
    BitrixAPINotFound,
    BitrixAPIOverloadLimit,
    BitrixAPIQueryLimitExceeded,
    BitrixAPIServiceUnavailable,
    BitrixAPIUnauthorized,
    BitrixAPIUserAccessError,
    BitrixOAuthInvalidClient,
    BitrixOAuthInvalidGrant,
    BitrixOAuthInvalidScope,
    BitrixOauthWrongClient,
    BitrixResponseJSONDecodeError,
)
from ...utils.types import JSONDict

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
    "EXPIRED_TOKEN": BitrixAPIExpiredToken,
    "NO_AUTH_FOUND": BitrixAPINoAuthFound,
    # 403
    "ACCESS_DENIED": BitrixAPIAccessDenied,
    "ALLOWED_ONLY_INTRANET_USER": BitrixAPIAllowedOnlyIntranetUser,
    "INSUFFICIENT_SCOPE": BitrixAPIInsufficientScope,
    "INVALID_CREDENTIALS": BitrixAPIInvalidCredentials,
    "INVALID_SCOPE": BitrixOAuthInvalidScope,
    "USER_ACCESS_ERROR": BitrixAPIUserAccessError,
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
    BitrixAPIInternalServerError.STATUS_CODE: BitrixAPIInternalServerError,  # 500
    BitrixAPIServiceUnavailable.STATUS_CODE: BitrixAPIServiceUnavailable,  # 503
    BitrixAPIMethodNotAllowed.STATUS_CODE: BitrixAPIMethodNotAllowed,  # 405
    BitrixAPINotFound.STATUS_CODE: BitrixAPINotFound,  # 404
    BitrixAPIForbidden.STATUS_CODE: BitrixAPIForbidden,  # 403
    BitrixAPIUnauthorized.STATUS_CODE: BitrixAPIUnauthorized,  # 401
    BitrixAPIBadRequest.STATUS_CODE: BitrixAPIBadRequest,  # 400
}
""""""


def _raise_http_error(response: requests.Response):
    raise HTTPError(
        f"{response.status_code} Client Error: {response.json()['error']} for url: {response.url}",
        response=response,
    )


def parse_response(response: requests.Response) -> JSONDict:
    """
    Parses the response from the API server. If response body contains an error message, raises appropriate exception

    Args:
        response: response returned by the API server

    Returns:
        dictionary containing the parsed response of the API server

    Raises:
        BitrixAPIError: base class for all API-related errors. Depening on an error code and/or an HTTP status code, more specific exception subclassed from BitrixAPIError will be raised.
                        These exceptions indicate that the API server successfully processed the response, but some occured during API method execution.
        BitrixResponseJSONDecodeError: if response returned by the API server is not a valid JSON
    """

    try:
        response.raise_for_status()
        json_response = response.json()

        if "error" in json_response:
            _raise_http_error(response)

    except HTTPError:
        try:
            json_response = response.json()
            error = str(json_response.get("error", ""))

            exception_class = (
                    _EXCEPTIONS_BY_ERROR.get(error.upper()) or
                    _EXCEPTIONS_BY_STATUS_CODE.get(response.status_code) or
                    BitrixAPIError
            )

            raise exception_class(json_response, response)

        except JSONDecodeError as error:
            raise BitrixResponseJSONDecodeError(original_error=error, response=response) from error

    else:
        return json_response
