import abc
import typing
from http import HTTPStatus as _HTTPStatus
from urllib.parse import urlparse as _urlparse

import requests

from .utils import types as _types

__all__ = [
    "BitrixAPIAccessDenied",
    "BitrixAPIAllowedOnlyIntranetUser",
    "BitrixAPIBadRequest",
    "BitrixAPIError",
    "BitrixAPIErrorBatchLengthExceeded",
    "BitrixAPIErrorBatchMethodNotAllowed",
    "BitrixAPIErrorManifestIsNotAvailable",
    "BitrixAPIErrorOAuth",
    "BitrixAPIErrorUnexpectedAnswer",
    "BitrixAPIExpiredToken",
    "BitrixAPIForbidden",
    "BitrixAPIInsufficientScope",
    "BitrixAPIInternalServerError",
    "BitrixAPIInvalidArgValue",
    "BitrixAPIInvalidCredentials",
    "BitrixAPIInvalidRequest",
    "BitrixAPIMethodConfirmDenied",
    "BitrixAPIMethodConfirmWaiting",
    "BitrixAPIMethodNotAllowed",
    "BitrixAPINoAuthFound",
    "BitrixAPINotFound",
    "BitrixAPIOverloadLimit",
    "BitrixAPIQueryLimitExceeded",
    "BitrixAPIServiceUnavailable",
    "BitrixAPIUnauthorized",
    "BitrixAPIUserAccessError",
    "BitrixOAuthException",
    "BitrixOAuthInsufficientScope",
    "BitrixOAuthInvalidClient",
    "BitrixOAuthInvalidGrant",
    "BitrixOAuthInvalidRequest",
    "BitrixOAuthInvalidScope",
    "BitrixOAuthRequestError",
    "BitrixOAuthRequestTimeout",
    "BitrixOauthWrongClient",
    "BitrixRequestError",
    "BitrixRequestTimeout",
    "BitrixResponse302JSONDecodeError",
    "BitrixResponse500JSONDecodeError",
    "BitrixResponseJSONDecodeError",
    "BitrixSDKException",
    "BitrixValidationError",
]


class _HTTPResponse(abc.ABC):
    """"""

    STATUS_CODE: _HTTPStatus = NotImplemented

    response: requests.Response

    @property
    def status_code(self) -> int:
        """"""
        return self.response.status_code


class _HTTPResponseOK(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.OK


class _HTTPResponseFound(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.FOUND


class _HTTPResponseBadRequest(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.BAD_REQUEST


class _HTTPResponseUnauthorized(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.UNAUTHORIZED


class _HTTPResponseForbidden(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.FORBIDDEN


class _HTTPResponseNotFound(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.NOT_FOUND


class _HTTPResponseMethodNotAllowed(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.METHOD_NOT_ALLOWED


class _HTTPResponseInternalError(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.INTERNAL_SERVER_ERROR


class _HTTPResponseServiceUnavailable(_HTTPResponse):
    """"""
    STATUS_CODE = _HTTPStatus.SERVICE_UNAVAILABLE


class BitrixSDKException(Exception):
    """BaseEntity class for all bitrix API exceptions."""

    __slots__ = ("message",)

    def __init__(self, message: typing.Text, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> typing.Text:
        return self.message


class BitrixOAuthException(BitrixSDKException):
    """"""


class BitrixValidationError(BitrixSDKException):
    """"""


class BitrixRequestError(BitrixSDKException):
    """A Connection error occurred."""

    __slots__ = ("original_error",)

    def __init__(self, original_error: Exception, *args):
        super().__init__(f"{self.__class__.__name__}: {original_error}", original_error, *args)
        self.original_error = original_error


class BitrixOAuthRequestError(BitrixRequestError, BitrixOAuthException):
    """"""


class BitrixRequestTimeout(BitrixRequestError):
    """"""

    __slots__ = ("timeout",)

    def __init__(self, original_error: Exception, timeout: int):
        super().__init__(original_error, timeout)
        self.timeout = timeout


class BitrixOAuthRequestTimeout(BitrixRequestTimeout, BitrixOAuthException):
    """"""


class BitrixResponseJSONDecodeError(BitrixRequestError, _HTTPResponse):
    """"""

    __slots__ = ("response",)

    def __init__(self, original_error: Exception, response: requests.Response):
        super().__init__(original_error, response)
        self.response = response


class BitrixResponse302JSONDecodeError(BitrixResponseJSONDecodeError, _HTTPResponseFound):
    """"""

    @property
    def redirect_url(self) -> typing.Optional[typing.Text]:
        """"""
        return self.response.headers.get("Location")

    @property
    def new_domain(self) -> typing.Optional[typing.Text]:
        """"""
        redirect_url = self.redirect_url
        return redirect_url and _urlparse(redirect_url).hostname


class BitrixResponse500JSONDecodeError(BitrixResponseJSONDecodeError, _HTTPResponseInternalError):
    """"""


class BitrixAPIError(BitrixSDKException, _HTTPResponse):
    """"""

    ERROR: typing.Text = NotImplemented

    __slots__ = ("json_response", "response")

    def __init__(self, json_response: _types.JSONDict, response: requests.Response):
        message = json_response.get("error_description", f"{self.__class__.__name__}: {response.text}")
        super().__init__(message, json_response, response)
        self.json_response = json_response
        self.response = response

    @property
    def error(self) -> typing.Text:
        """"""
        return self.json_response.get("error", "")

    @property
    def error_description(self) -> typing.Text:
        """"""
        return self.json_response.get("error_description", "")


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError, _HTTPResponseBadRequest):
    """Bad Request."""


class BitrixAPIUnauthorized(BitrixAPIError, _HTTPResponseUnauthorized):
    """Unauthorized."""


class BitrixAPIForbidden(BitrixAPIError, _HTTPResponseForbidden):
    """Forbidden."""


class BitrixAPINotFound(BitrixAPIError, _HTTPResponseNotFound):
    """Not Found."""
    ERROR = "NOT_FOUND"


class BitrixAPIMethodNotAllowed(BitrixAPIError, _HTTPResponseMethodNotAllowed):
    """Method Not Allowed."""


class BitrixAPIInternalServerError(BitrixAPIError, _HTTPResponseInternalError):
    """Internal server error."""
    ERROR = "INTERNAL_SERVER_ERROR"


class BitrixAPIServiceUnavailable(BitrixAPIError, _HTTPResponseServiceUnavailable):
    """Service Unavailable."""


# Exceptions by error

# 200

class BitrixOauthWrongClient(BitrixAPIError, BitrixOAuthException, _HTTPResponseOK):
    """Wrong client"""
    ERROR = "WRONG_CLIENT"


# 400

class BitrixAPIErrorBatchLengthExceeded(BitrixAPIBadRequest):
    """Max batch length exceeded."""
    ERROR = "ERROR_BATCH_LENGTH_EXCEEDED"


class BitrixAPIInvalidArgValue(BitrixAPIBadRequest):
    """"""
    ERROR = "INVALID_ARG_VALUE"


class BitrixAPIInvalidRequest(BitrixAPIBadRequest):
    """Https required."""
    ERROR = "INVALID_REQUEST"


class BitrixOAuthInvalidRequest(BitrixAPIInvalidRequest, BitrixOAuthException):
    """An incorrectly formatted authorization requests was provided"""


class BitrixOAuthInvalidClient(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid client data was provided. The application may not be installed in Bitrix24"""
    ERROR = "INVALID_CLIENT"


class BitrixOAuthInvalidGrant(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid authorization tokens were provided when obtaining access_token. This occurs during renewal or initial acquisition"""
    ERROR = "INVALID_GRANT"


# 401

class BitrixAPIErrorOAuth(BitrixAPIUnauthorized):
    """Application not installed."""
    ERROR = "ERROR_OAUTH"


class BitrixAPIExpiredToken(BitrixAPIUnauthorized):
    """The access token provided has expired."""
    ERROR = "EXPIRED_TOKEN"


class BitrixAPIMethodConfirmWaiting(BitrixAPIUnauthorized):
    """Waiting for confirmation."""
    ERROR = "METHOD_CONFIRM_WAITING"


class BitrixAPINoAuthFound(BitrixAPIUnauthorized):
    """Wrong authorization data."""
    ERROR = "NO_AUTH_FOUND"


# 403

class BitrixAPIAccessDenied(BitrixAPIForbidden):
    """REST API is available only on commercial plans."""
    ERROR = "ACCESS_DENIED"


class BitrixAPIAllowedOnlyIntranetUser(BitrixAPIForbidden):
    """"""
    ERROR = "ALLOWED_ONLY_INTRANET_USER"


class BitrixAPIInsufficientScope(BitrixAPIForbidden):
    """The request requires higher privileges than provided by the webhook token."""
    ERROR = "INSUFFICIENT_SCOPE"


class BitrixAPIInvalidCredentials(BitrixAPIForbidden):
    """Invalid requests credentials."""
    ERROR = "INVALID_CREDENTIALS"


class BitrixAPIMethodConfirmDenied(BitrixAPIForbidden):
    """Method call denied."""
    ERROR = "METHOD_CONFIRM_DENIED"


class BitrixAPIUserAccessError(BitrixAPIForbidden):
    """The user does not have acfcess to the application."""
    ERROR = "USER_ACCESS_ERROR"


class BitrixOAuthInvalidScope(BitrixAPIForbidden, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card"""
    ERROR = "INVALID_SCOPE"


class BitrixOAuthInsufficientScope(BitrixAPIInsufficientScope, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card"""


# 404

class BitrixAPIErrorManifestIsNotAvailable(BitrixAPINotFound):
    """Manifest is not available"""
    ERROR = "ERROR_MANIFEST_IS_NOT_AVAILABLE"


# 405

class BitrixAPIErrorBatchMethodNotAllowed(BitrixAPIMethodNotAllowed):
    """Method is not allowed for batch usage."""
    ERROR = "ERROR_BATCH_METHOD_NOT_ALLOWED"


# 500

class BitrixAPIErrorUnexpectedAnswer(BitrixAPIInternalServerError):
    """Server returned an unexpected responses."""
    ERROR = "ERROR_UNEXPECTED_ANSWER"


# 503

class BitrixAPIOverloadLimit(BitrixAPIServiceUnavailable):
    """REST API is blocked due to overload."""
    ERROR = "OVERLOAD_LIMIT"


class BitrixAPIQueryLimitExceeded(BitrixAPIServiceUnavailable):
    """Too many requests."""
    ERROR = "QUERY_LIMIT_EXCEEDED"
