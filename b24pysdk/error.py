from http import HTTPStatus
import requests
from typing import Text

from .utils.types import JSONDict


class BitrixSDKException(Exception):
    """Base class for all bitrix API exceptions."""

    __slots__ = ("message",)

    def __init__(self, message: Text, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> Text:
        return self.message


class RequestToBitrixError(BitrixSDKException):
    """A Connection error occurred."""

    __slots__ = ("original_error",)

    def __init__(self, original_error: Exception, *args):
        super().__init__(f"{self.__class__.__name__}: {original_error}", original_error, *args)
        self.original_error = original_error


class BitrixTimeout(RequestToBitrixError):
    """"""

    __slots__ = ("timeout",)

    STATUS_CODE: int = HTTPStatus.GATEWAY_TIMEOUT

    def __init__(self, original_error: Exception, timeout: int):
        super().__init__(original_error, timeout)
        self.timeout = timeout


class BitrixApiError(BitrixSDKException):
    """"""

    __slots__ = ("json_response", "response")

    def __init__(self, json_response: JSONDict, response: requests.Response):
        message = json_response.get("error_description", f"{self.__class__.__name__}: {response.text}")
        super().__init__(message, json_response, response)
        self.json_response = json_response
        self.response = response

    @property
    def status_code(self) -> int:
        """"""
        return self.response.status_code

    @property
    def error(self) -> Text:
        """"""
        return self.json_response.get("error")

    @property
    def error_description(self) -> Text:
        """"""
        return self.json_response.get("error_description")


# Exceptions by status code

class BitrixApiBadRequest(BitrixApiError):
    """Bad Request."""

    STATUS_CODE: int = HTTPStatus.BAD_REQUEST


class BitrixApiUnauthorized(BitrixApiError):
    """Unauthorized."""

    STATUS_CODE: int = HTTPStatus.UNAUTHORIZED


class BitrixApiForbidden(BitrixApiError):
    """Forbidden."""

    STATUS_CODE: int = HTTPStatus.FORBIDDEN


class BitrixApiNotFound(BitrixApiError):
    """Not Found."""

    STATUS_CODE: int = HTTPStatus.NOT_FOUND


class BitrixApiMethodNotAllowed(BitrixApiError):
    """Method Not Allowed."""

    STATUS_CODE: int = HTTPStatus.METHOD_NOT_ALLOWED


class BitrixApiInternalServerError(BitrixApiError):
    """Internal server error."""

    STATUS_CODE: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ERROR: Text = "INTERNAL_SERVER_ERROR"


class BitrixApiServiceUnavailable(BitrixApiError):
    """Service Unavailable."""

    STATUS_CODE: int = HTTPStatus.SERVICE_UNAVAILABLE


# Exceptions by error

# 400

class BitrixApiErrorBatchLengthExceeded(BitrixApiBadRequest):
    """Max batch length exceeded."""

    ERROR: Text = "ERROR_BATCH_LENGTH_EXCEEDED"


class BitrixApiInvalidRequest(BitrixApiBadRequest):
    """Https required."""

    ERROR: Text = "INVALID_REQUEST"


# 401

class BitrixApiExpiredToken(BitrixApiUnauthorized):
    """The access token provided has expired."""

    ERROR: Text = "EXPIRED_TOKEN"


class BitrixApiNoAuthFound(BitrixApiUnauthorized):
    """Wrong authorization data."""

    ERROR: Text = "NO_AUTH_FOUND"


# 403

class BitrixApiAccessDenied(BitrixApiForbidden):
    """REST API is available only on commercial plans."""

    ERROR: Text = "ACCESS_DENIED"


class BitrixApiInsufficientScope(BitrixApiForbidden):
    """The request requires higher privileges than provided by the webhook token."""

    ERROR: Text = "INSUFFICIENT_SCOPE"


class BitrixApiInvalidCredentials(BitrixApiForbidden):
    """Invalid request credentials."""

    ERROR: Text = "INVALID_CREDENTIALS"


class BitrixApiUserAccessError(BitrixApiForbidden):
    """The user does not have access to the application."""

    ERROR: Text = "USER_ACCESS_ERROR"


# 404

class BitrixApiErrorManifestIsNotAvailable(BitrixApiNotFound):
    """Manifest is not available"""

    ERROR: Text = "ERROR_MANIFEST_IS_NOT_AVAILABLE"


# 405

class BitrixApiErrorBatchMethodNotAllowed(BitrixApiMethodNotAllowed):
    """Method is not allowed for batch usage."""

    ERROR: Text = "ERROR_BATCH_METHOD_NOT_ALLOWED"


# 500

class BitrixApiErrorUnexpectedAnswer(BitrixApiInternalServerError):
    """Server returned an unexpected response."""

    ERROR: Text = "ERROR_UNEXPECTED_ANSWER"


# 503

class BitrixApiOverloadLimit(BitrixApiServiceUnavailable):
    """REST API is blocked due to overload."""

    ERROR: Text = "OVERLOAD_LIMIT"


class BitrixApiQueryLimitExceeded(BitrixApiServiceUnavailable):
    """Too many requests."""

    ERROR: Text = "QUERY_LIMIT_EXCEEDED"
