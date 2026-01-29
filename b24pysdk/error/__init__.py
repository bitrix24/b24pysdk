import typing
from urllib.parse import urlparse as _urlparse

import requests

from ._http_response import (
    HTTPResponse,
    HTTPResponseBadRequest,
    HTTPResponseForbidden,
    HTTPResponseFound,
    HTTPResponseInternalError,
    HTTPResponseMethodNotAllowed,
    HTTPResponseNotFound,
    HTTPResponseOK,
    HTTPResponseServiceUnavailable,
    HTTPResponseTooManyRequests,
    HTTPResponseUnauthorized,
)

if typing.TYPE_CHECKING:
    from ..utils import types as _types

__all__ = [
    "BaseBitrixAPIError",
    "BitrixAPIAccessDenied",
    "BitrixAPIAllowedOnlyIntranetUser",
    "BitrixAPIAuthorizationError",
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
    "BitrixAPIOperationTimeLimit",
    "BitrixAPIOverloadLimit",
    "BitrixAPIQueryLimitExceeded",
    "BitrixAPIServiceUnavailable",
    "BitrixAPIUnauthorized",
    "BitrixAPIUserAccessError",
    "BitrixAPIWrongAuthType",
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
    "BitrixResponse403JSONDecodeError",
    "BitrixResponse500JSONDecodeError",
    "BitrixResponseJSONDecodeError",
    "BitrixSDKException",
    "BitrixValidationError",
]


class BitrixSDKException(Exception):
    """Base class for all bitrix API exceptions."""

    __slots__ = ("message",)

    message: typing.Text

    def __init__(self, message: typing.Text, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> typing.Text:
        return self.message


class BitrixOAuthException(BitrixSDKException):
    """"""


class BitrixValidationError(BitrixSDKException, ValueError):
    """"""


class BitrixRequestError(BitrixSDKException):
    """A Connection error occurred."""

    __slots__ = ("original_error",)

    original_error: Exception

    def __init__(self, original_error: Exception, *args):
        super().__init__(f"{self.__class__.__name__}: {original_error}", original_error, *args)
        self.original_error = original_error


class BitrixOAuthRequestError(BitrixRequestError, BitrixOAuthException):
    """An error occurred during an OAuth operation.

    This exception typically occurs when there is an issue with the OAuth request, possibly due to incorrect parameters or network-related issues.
    """


class BitrixRequestTimeout(BitrixRequestError):
    """A timeout occurred while waiting for an API response.

    Raised when the server takes too long to respond, often indicating network congestion or server-side delays.
    """

    __slots__ = ("timeout",)

    timeout: "_types.DefaultTimeout"

    def __init__(self, original_error: Exception, timeout: "_types.DefaultTimeout"):
        super().__init__(original_error, timeout)
        self.timeout = timeout


class BitrixOAuthRequestTimeout(BitrixRequestTimeout, BitrixOAuthException):
    """"""


class BitrixResponseJSONDecodeError(BitrixRequestError, HTTPResponse):
    """"""

    __slots__ = ("response",)

    def __init__(self, original_error: Exception, response: requests.Response):
        super().__init__(original_error, response)
        self.response = response


class BitrixResponse302JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseFound):
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


class BitrixResponse403JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseForbidden):
    """"""


class BitrixResponse500JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseInternalError):
    """"""


class BaseBitrixAPIError(BitrixSDKException, HTTPResponse):
    """"""

    __slots__ = ("json_response", "response")

    json_response: "_types.JSONDict"

    def __init__(self, json_response: "_types.JSONDict", response: requests.Response):
        error = json_response.get("error")

        if isinstance(error, dict):
            message = error.get("message", f"{self.__class__.__name__}: {response.text}")
        else:
            message = json_response.get("error_description", f"{self.__class__.__name__}: {response.text}")

        super().__init__(message, json_response, response)

        self.json_response = json_response
        self.response = response


# ------------------------ Exceptions for API v1 and v2 ------------------------


class BitrixAPIError(BaseBitrixAPIError):
    """"""

    ERROR: typing.ClassVar[typing.Text] = NotImplemented

    __slots__ = ()

    @property
    def error(self) -> typing.Text:
        """"""
        return self.json_response.get("error", "")

    @property
    def error_description(self) -> typing.Text:
        """"""
        return self.json_response.get("error_description", "")


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError, HTTPResponseBadRequest):
    """Bad Request."""


class BitrixAPIUnauthorized(BitrixAPIError, HTTPResponseUnauthorized):
    """Unauthorized."""


class BitrixAPIForbidden(BitrixAPIError, HTTPResponseForbidden):
    """Forbidden."""


class BitrixAPINotFound(BitrixAPIError, HTTPResponseNotFound):
    """Not Found.

    Raised when the specified resource cannot be located on the server.
    """
    ERROR = "NOT_FOUND"


class BitrixAPIMethodNotAllowed(BitrixAPIError, HTTPResponseMethodNotAllowed):
    """Method Not Allowed.

    Indicates that the HTTP method used in the request is not allowed for the requested resource.
    """


class BitrixAPIInternalServerError(BitrixAPIError, HTTPResponseInternalError):
    """Internal server error."""
    ERROR = "INTERNAL_SERVER_ERROR"


class BitrixAPIServiceUnavailable(BitrixAPIError, HTTPResponseServiceUnavailable):
    """Service Unavailable.

    Raised when the API service is temporarily unavailable, often due to maintenance or server overload.
    """


# Exceptions by error

# 200

class BitrixOauthWrongClient(BitrixAPIError, BitrixOAuthException, HTTPResponseOK):
    """Wrong client"""
    ERROR = "WRONG_CLIENT"


# 400

class BitrixAPIErrorBatchLengthExceeded(BitrixAPIBadRequest):
    """Max batch length exceeded.

    Raised when the number of operations in a batch exceeds the allowable maximum length.
    """
    ERROR = "ERROR_BATCH_LENGTH_EXCEEDED"


class BitrixAPIInvalidArgValue(BitrixAPIBadRequest):
    """Invalid argument value provided.

    Raised when one or more arguments in the request contain invalid values, which the server cannot process.
    """
    ERROR = "INVALID_ARG_VALUE"


class BitrixAPIInvalidRequest(BitrixAPIBadRequest):
    """Https required.

    Indicates the request was formatted incorrectly, often requiring an HTTPS connection rather than HTTP.
    """
    ERROR = "INVALID_REQUEST"


class BitrixOAuthInvalidRequest(BitrixAPIInvalidRequest, BitrixOAuthException):
    """An incorrectly formatted authorization requests was provided"""


class BitrixOAuthInvalidClient(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid client data was provided. The application may not be installed in Bitrix24"""
    ERROR = "INVALID_CLIENT"


class BitrixOAuthInvalidGrant(BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid authorization tokens were provided when obtaining access_token.

    This occurs during renewal or initial acquisition, indicating the provided tokens cannot be validated.
    """
    ERROR = "INVALID_GRANT"


# 401

class BitrixAPIAuthorizationError(BitrixAPIUnauthorized):
    """Unable to authorize user.

    This exception indicates a failure to authenticate the user, potentially due to missing or incorrect credentials.
    """
    ERROR = "AUTHORIZATION_ERROR"


class BitrixAPIErrorOAuth(BitrixAPIUnauthorized):
    """Application not installed.

    Indicates that the operation cannot proceed because the application is not installed in the Bitrix environment.
    """
    ERROR = "ERROR_OAUTH"


class BitrixAPIExpiredToken(BitrixAPIUnauthorized):
    """The access token provided has expired.

    This exception is raised when a request is made using an OAuth token that has exceeded its validity period.
    Handling this properly often involves refreshing the token to regain access as per the OAuth 2.0 logic.
    """
    ERROR = "EXPIRED_TOKEN"


class BitrixAPIMethodConfirmWaiting(BitrixAPIUnauthorized):
    """Waiting for confirmation.

    Raised when an API call requires a user to confirm their action, and the confirmation is still pending.
    """
    ERROR = "METHOD_CONFIRM_WAITING"


class BitrixAPINoAuthFound(BitrixAPIUnauthorized):
    """Wrong authorization data.

    This exception signals that no valid authentication was found in the request context.
    """
    ERROR = "NO_AUTH_FOUND"


# 403

class BitrixAPIAccessDenied(BitrixAPIForbidden):
    """REST API is available only on commercial plans."""
    ERROR = "ACCESS_DENIED"


class BitrixAPIAllowedOnlyIntranetUser(BitrixAPIForbidden):
    """"""
    ERROR = "ALLOWED_ONLY_INTRANET_USER"


class BitrixAPIInsufficientScope(BitrixAPIForbidden):
    """The request requires higher privileges than provided by the webhook token.

    Raised when an operation requires more permissions than the current token's access level allows.
    """
    ERROR = "INSUFFICIENT_SCOPE"


class BitrixAPIInvalidCredentials(BitrixAPIForbidden):
    """Invalid request credentials.

    Indicates the credentials provided in the request are not valid for accessing the requested resource or action.
    """
    ERROR = "INVALID_CREDENTIALS"


class BitrixAPIMethodConfirmDenied(BitrixAPIForbidden):
    """Method call denied.

    Raised when a confirmation-required method is denied by the user.
    """
    ERROR = "METHOD_CONFIRM_DENIED"


class BitrixAPIUserAccessError(BitrixAPIForbidden):
    """The user does not have acfcess to the application."""
    ERROR = "USER_ACCESS_ERROR"


class BitrixAPIWrongAuthType(BitrixAPIForbidden):
    """Current authorization type is denied for this method."""
    ERROR = "WRONG_AUTH_TYPE"


class BitrixOAuthInvalidScope(BitrixAPIForbidden, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card.

    This occurs when the scope of access specified in the OAuth request is greater than what is allowed by the application configuration.
    """
    ERROR = "INVALID_SCOPE"


class BitrixOAuthInsufficientScope(BitrixAPIInsufficientScope, BitrixOAuthException):
    """Access permissions requested exceed those specified in the application card"""


# 404

class BitrixAPIErrorManifestIsNotAvailable(BitrixAPINotFound):
    """Manifest is not available.

    Raised when a requested manifest file cannot be located or retrieved from the Bitrix server.
    """
    ERROR = "ERROR_MANIFEST_IS_NOT_AVAILABLE"


# 405

class BitrixAPIErrorBatchMethodNotAllowed(BitrixAPIMethodNotAllowed):
    """Method is not allowed for batch usage.

    Raised when a specific method cannot be used within a batch operation.
    """
    ERROR = "ERROR_BATCH_METHOD_NOT_ALLOWED"


# 429

class BitrixAPIOperationTimeLimit(BitrixAPIError, HTTPResponseTooManyRequests):
    """Method is blocked due to operation time limit."""
    ERROR = "OPERATION_TIME_LIMIT"


# 500

class BitrixAPIErrorUnexpectedAnswer(BitrixAPIInternalServerError):
    """Server returned an unexpected response.

    Raised when the server's response is not in the expected format, which can occur during server-side issues.
    """
    ERROR = "ERROR_UNEXPECTED_ANSWER"


# 503

class BitrixAPIOverloadLimit(BitrixAPIServiceUnavailable):
    """REST API is blocked due to overload.

    Raised when the API service blocks further requests, typically due to traffic exceeding safe operational limits.
    """
    ERROR = "OVERLOAD_LIMIT"


class BitrixAPIQueryLimitExceeded(BitrixAPIServiceUnavailable):
    """Too many requests.

    Raised when the number of API requests exceeds the allowed limit, prompting the client to slow down the request rate.
    """
    ERROR = "QUERY_LIMIT_EXCEEDED"
