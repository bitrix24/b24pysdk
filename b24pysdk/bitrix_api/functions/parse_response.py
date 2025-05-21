import requests
from requests.exceptions import HTTPError, JSONDecodeError
from typing import Dict, Text, Type

from ...utils.types import JSONDict

from ...error import (
    BitrixApiError,
    BitrixApiErrorUnexpectedAnswer,
    BitrixApiQueryLimitExceeded,
    BitrixApiErrorBatchMethodNotAllowed,
    BitrixApiErrorBatchLengthExceeded,
    BitrixApiNoAuthFound,
    BitrixApiInvalidRequest,
    BitrixApiOverloadLimit,
    BitrixApiAccessDenied,
    BitrixApiInvalidCredentials,
    BitrixApiErrorManifestIsNotAvailable,
    BitrixApiInsufficientScope,
    BitrixApiExpiredToken,
    BitrixApiUserAccessError,
    BitrixApiInternalServerError,
    BitrixApiServiceUnavailable,
    BitrixApiMethodNotAllowed,
    BitrixApiNotFound,
    BitrixApiForbidden,
    BitrixApiUnauthorized,
    BitrixApiBadRequest,
)


_EXCEPTIONS_BY_ERROR: Dict[Text, Type[BitrixApiError]] = {
    # 400
    "ERROR_BATCH_LENGTH_EXCEEDED": BitrixApiErrorBatchLengthExceeded,
    "INVALID_REQUEST": BitrixApiInvalidRequest,
    # 401
    "EXPIRED_TOKEN": BitrixApiExpiredToken,
    "NO_AUTH_FOUND": BitrixApiNoAuthFound,
    # 403
    "ACCESS_DENIED": BitrixApiAccessDenied,
    "INSUFFICIENT_SCOPE": BitrixApiInsufficientScope,
    "INVALID_CREDENTIALS": BitrixApiInvalidCredentials,
    "USER_ACCESS_ERROR": BitrixApiUserAccessError,
    # 404
    "ERROR_MANIFEST_IS_NOT_AVAILABLE": BitrixApiErrorManifestIsNotAvailable,
    # 405
    "ERROR_BATCH_METHOD_NOT_ALLOWED": BitrixApiErrorBatchMethodNotAllowed,
    # 500
    "ERROR_UNEXPECTED_ANSWER": BitrixApiErrorUnexpectedAnswer,
    "INTERNAL_SERVER_ERROR": BitrixApiInternalServerError,
    # 503
    "OVERLOAD_LIMIT": BitrixApiOverloadLimit,
    "QUERY_LIMIT_EXCEEDED": BitrixApiQueryLimitExceeded,
}
""""""

_EXCEPTIONS_BY_STATUS_CODE: Dict[int, Type[BitrixApiError]] = {
    BitrixApiInternalServerError.STATUS_CODE: BitrixApiInternalServerError,  # 500
    BitrixApiServiceUnavailable.STATUS_CODE: BitrixApiServiceUnavailable,    # 503
    BitrixApiMethodNotAllowed.STATUS_CODE: BitrixApiMethodNotAllowed,        # 405
    BitrixApiNotFound.STATUS_CODE: BitrixApiNotFound,                        # 404
    BitrixApiForbidden.STATUS_CODE: BitrixApiForbidden,                      # 403
    BitrixApiUnauthorized.STATUS_CODE: BitrixApiUnauthorized,                # 401
    BitrixApiBadRequest.STATUS_CODE: BitrixApiBadRequest,                    # 400
}
""""""


def parse_response(response: requests.Response) -> JSONDict:
    """
    Checks if response body contains an error message and raises appropriate exception
    """

    try:
        response.raise_for_status()
        return response.json()

    except HTTPError:
        try:
            json_response = response.json()
            error = json_response.get("error")

            exception_class = _EXCEPTIONS_BY_ERROR.get(error) or _EXCEPTIONS_BY_STATUS_CODE.get(response.status_code) or BitrixApiError

            raise exception_class(json_response, response)

        except JSONDecodeError:
            raise   # TODO
