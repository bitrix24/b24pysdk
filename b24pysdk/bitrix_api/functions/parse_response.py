from typing import Dict, Text, Type

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from ...error import (
    BitrixAPIAccessDenied,
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
    "INVALID_CLIENT": BitrixOAuthInvalidClient,
    "INVALID_GRANT": BitrixOAuthInvalidGrant,
    "INVALID_REQUEST": BitrixAPIInvalidRequest,
    # 401
    "EXPIRED_TOKEN": BitrixAPIExpiredToken,
    "NO_AUTH_FOUND": BitrixAPINoAuthFound,
    # 403
    "ACCESS_DENIED": BitrixAPIAccessDenied,
    "INSUFFICIENT_SCOPE": BitrixAPIInsufficientScope,
    "INVALID_CREDENTIALS": BitrixAPIInvalidCredentials,
    "INVALID_SCOPE": BitrixOAuthInvalidScope,
    "USER_ACCESS_ERROR": BitrixAPIUserAccessError,
    # 404
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
    Checks if response body contains an error message and raises appropriate exception
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
