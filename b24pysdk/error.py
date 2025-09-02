import typing
from http import HTTPStatus as _HTTPStatus

import requests

from .utils.types import JSONDict as _JSONDict


class BitrixSDKException(Exception):
    """Base class for all bitrix API exceptions."""

    __slots__ = ("message",)

    def __init__(self, message: typing.Text, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> typing.Text:
        return self.message


class BitrixOAuthException(BitrixSDKException):
    """"""


class BitrixRequestError(BitrixSDKException):
    """A Connection error occurred."""

    __slots__ = ("original_error",)

    def __init__(self, original_error: Exception, *args):
        super().__init__(f"{self.__class__.__name__}: {original_error}", original_error, *args)
        self.original_error = original_error


class BitrixOAuthRequestError(BitrixRequestError, BitrixOAuthException):
    """"""


class BitrixTimeout(BitrixRequestError):
    """"""

    __slots__ = ("timeout",)

    STATUS_CODE: int = _HTTPStatus.GATEWAY_TIMEOUT

    def __init__(self, original_error: Exception, timeout: int):
        super().__init__(original_error, timeout)
        self.timeout = timeout


class BitrixOAuthTimeout(BitrixTimeout, BitrixOAuthException):
    """"""


class BitrixResponseJSONDecodeError(BitrixRequestError):
    """"""

    __slots__ = ("response",)

    def __init__(self, original_error: Exception, response: requests.Response):
        super().__init__(original_error, response)
        self.response = response

    @property
    def status_code(self) -> int:
        """"""
        return self.response.status_code


class BitrixAPIError(BitrixSDKException):
    """"""

    __slots__ = ("json_response", "response")

    def __init__(self, json_response: _JSONDict, response: requests.Response):
        message = json_response.get("error_description", f"{self.__class__.__name__}: {response.text}")
        super().__init__(message, json_response, response)
        self.json_response = json_response
        self.response = response

    @property
    def status_code(self) -> int:
        """"""
        return self.response.status_code

    @property
    def error(self) -> typing.Text:
        """"""
        return self.json_response.get("error")

    @property
    def error_description(self) -> typing.Text:
        """"""
        return self.json_response.get("error_description")


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError):
    """Bad Request."""

    STATUS_CODE: int = _HTTPStatus.BAD_REQUEST


class BitrixAPIUnauthorized(BitrixAPIError):
    """Unauthorized."""

    STATUS_CODE: int = _HTTPStatus.UNAUTHORIZED


class BitrixAPIForbidden(BitrixAPIError):
    """Forbidden."""

    STATUS_CODE: int = _HTTPStatus.FORBIDDEN


class BitrixAPINotFound(BitrixAPIError):
    """Not Found."""

    STATUS_CODE: int = _HTTPStatus.NOT_FOUND
    ERROR: typing.Text = "NOT_FOUND"


class BitrixAPIMethodNotAllowed(BitrixAPIError):
    """Method Not Allowed."""

    STATUS_CODE: int = _HTTPStatus.METHOD_NOT_ALLOWED


class BitrixAPIInternalServerError(BitrixAPIError):
    """Internal server error."""

    STATUS_CODE: int = _HTTPStatus.INTERNAL_SERVER_ERROR
    ERROR: typing.Text = "INTERNAL_SERVER_ERROR"


class BitrixAPIServiceUnavailable(BitrixAPIError):
    """Service Unavailable."""

    STATUS_CODE: int = _HTTPStatus.SERVICE_UNAVAILABLE


# Exceptions by error

# 200

class BitrixOauthWrongClient(BitrixAPIError, BitrixOAuthException):
    """Wrong client"""

    ERROR = "WRONG_CLIENT"


# 400

class BitrixAPIErrorBatchLengthExceeded(BitrixAPIBadRequest):
    """Max batch length exceeded."""

    ERROR: typing.Text = "ERROR_BATCH_LENGTH_EXCEEDED"


class BitrixAPIInvalidArgValue(BitrixAPIBadRequest):
    """"""

    ERROR: typing.Text = "INVALID_ARG_VALUE"


class BitrixAPIInvalidRequest(BitrixAPIBadRequest):
    """Https required."""

    ERROR: typing.Text = "INVALID_REQUEST"


class BitrixOAuthInvalidRequest(BitrixAPIInvalidRequest, BitrixOAuthException):
    """An incorrectly formatted authorization request was provided"""


class BitrixOAuthInvalidClient(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid client data was provided. The application may not be installed in Bitrix24"""

    ERROR = "INVALID_CLIENT"


class BitrixOAuthInvalidGrant(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid authorization tokens were provided when obtaining access_token. This occurs during renewal or initial acquisition"""

    ERROR = "INVALID_GRANT"


# 401

class BitrixAPIExpiredToken(BitrixAPIUnauthorized):
    """The access token provided has expired."""

    ERROR: typing.Text = "EXPIRED_TOKEN"


class BitrixAPINoAuthFound(BitrixAPIUnauthorized):
    """Wrong authorization data."""

    ERROR: typing.Text = "NO_AUTH_FOUND"


class BitrixAPIErrorOAUTH(BitrixAPIUnauthorized):
    """Application not installed."""

    ERROR: typing.Text = "ERROR_OAUTH"


# 403

class BitrixAPIAccessDenied(BitrixAPIForbidden):
    """REST API is available only on commercial plans."""

    ERROR: typing.Text = "ACCESS_DENIED"


class BitrixAPIAllowedOnlyIntranetUser(BitrixAPIForbidden):
    """"""

    ERROR: typing.Text = "ALLOWED_ONLY_INTRANET_USER"


class BitrixAPIInsufficientScope(BitrixAPIForbidden):
    """The request requires higher privileges than provided by the webhook token."""

    ERROR: typing.Text = "INSUFFICIENT_SCOPE"


class BitrixOAuthInvalidScope(BitrixAPIForbidden, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card"""

    ERROR: typing.Text = "INVALID_SCOPE"


class BitrixOAuthInsufficientScope(BitrixAPIInsufficientScope, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card"""


class BitrixAPIInvalidCredentials(BitrixAPIForbidden):
    """Invalid request credentials."""

    ERROR: typing.Text = "INVALID_CREDENTIALS"


class BitrixAPIUserAccessError(BitrixAPIForbidden):
    """The user does not have acfcess to the application."""

    ERROR: typing.Text = "USER_ACCESS_ERROR"


# 404

class BitrixAPIErrorManifestIsNotAvailable(BitrixAPINotFound):
    """Manifest is not available"""

    ERROR: typing.Text = "ERROR_MANIFEST_IS_NOT_AVAILABLE"


# 405

class BitrixAPIErrorBatchMethodNotAllowed(BitrixAPIMethodNotAllowed):
    """Method is not allowed for batch usage."""

    ERROR: typing.Text = "ERROR_BATCH_METHOD_NOT_ALLOWED"


# 500

class BitrixAPIErrorUnexpectedAnswer(BitrixAPIInternalServerError):
    """Server returned an unexpected response."""

    ERROR: typing.Text = "ERROR_UNEXPECTED_ANSWER"


# 503

class BitrixAPIOverloadLimit(BitrixAPIServiceUnavailable):
    """REST API is blocked due to overload."""

    ERROR: typing.Text = "OVERLOAD_LIMIT"


class BitrixAPIQueryLimitExceeded(BitrixAPIServiceUnavailable):
    """Too many requests."""

    ERROR: typing.Text = "QUERY_LIMIT_EXCEEDED"
