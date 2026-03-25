"""
Bitrix SDK exception hierarchy.

This module defines all exceptions raised by the Bitrix API client,
including:

- network errors
- HTTP errors
- JSON parsing errors
- Bitrix REST API errors
- OAuth errors

The exception hierarchy allows precise handling of API failures.
"""

import typing
from urllib.parse import urlparse as _urlparse

import requests

from ._http_responses import (
    HTTPResponse,
    HTTPResponseBadRequest,
    HTTPResponseForbidden,
    HTTPResponseFound,
    HTTPResponseGone,
    HTTPResponseInternalServerError,
    HTTPResponseMethodNotAllowed,
    HTTPResponseNotFound,
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
    "BitrixAPIApplicationNotFound",
    "BitrixAPIAuthorizationError",
    "BitrixAPIBadRequest",
    "BitrixAPIError",
    "BitrixAPIErrorOAuth",
    "BitrixAPIErrorUnexpectedAnswer",
    "BitrixAPIExpiredToken",
    "BitrixAPIForbidden",
    "BitrixAPIGone",
    "BitrixAPIInsufficientScope",
    "BitrixAPIInternalServerError",
    "BitrixAPIInvalidArgValue",
    "BitrixAPIInvalidCredentials",
    "BitrixAPIInvalidRequest",
    "BitrixAPIInvalidToken",
    "BitrixAPIMethodConfirmDenied",
    "BitrixAPIMethodConfirmWaiting",
    "BitrixAPIMethodNotAllowed",
    "BitrixAPINoAuthFound",
    "BitrixAPINotFound",
    "BitrixAPIOperationTimeLimit",
    "BitrixAPIOverloadLimit",
    "BitrixAPIPaymentRequired",
    "BitrixAPIPortalDeleted",
    "BitrixAPIQueryLimitExceeded",
    "BitrixAPIServiceUnavailable",
    "BitrixAPITooManyRequests",
    "BitrixAPIUnauthorized",
    "BitrixAPIUserAccessError",
    "BitrixAPIWrongAuthType",
    "BitrixRequestError",
    "BitrixRequestTimeout",
    "BitrixResponse302JSONDecodeError",
    "BitrixResponse403JSONDecodeError",
    "BitrixResponse500JSONDecodeError",
    "BitrixResponseError",
    "BitrixResponseJSONDecodeError",
    "BitrixSDKException",
    "BitrixValidationError",
]


class BitrixSDKException(Exception):
    """
    Base exception for all errors raised by the Bitrix SDK.

    This class is the root of the exception hierarchy used in the SDK.
    All Bitrix-related errors should inherit from this class.

    Parameters
    ----------
    message : Text
        Human-readable error message.
    """

    __slots__ = ("message",)

    message: typing.Text

    def __init__(self, message: typing.Text, *args):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> typing.Text:
        return self.message


class BitrixValidationError(BitrixSDKException, ValueError):
    """
    Raised when SDK input validation fails.

    This exception indicates incorrect argument values, invalid
    combinations of parameters, or malformed data detected before
    sending a request to Bitrix24.
    """

    __slots__ = ()


class BitrixRequestError(BitrixSDKException):
    """
    Raised when a network error occurs during an API request.

    This usually wraps exceptions raised by the `requests` library,
    such as connection failures or DNS resolution issues.

    Parameters
    ----------
    original_error : Exception
        The underlying exception raised by the HTTP client.
    """

    __slots__ = ()

    def __init__(self, original_error: Exception, *args):
        super().__init__(f"{self.__class__.__name__}: {original_error}", original_error, *args)


class BitrixRequestTimeout(BitrixRequestError):
    """
    Raised when a request to the Bitrix API exceeds the configured timeout.

    Attributes
    ----------
    timeout : DefaultTimeout
        Timeout value that was used for the request.
    """

    __slots__ = ("timeout",)

    timeout: "_types.DefaultTimeout"

    def __init__(self, original_error: Exception, timeout: "_types.DefaultTimeout"):
        super().__init__(original_error, timeout)
        self.timeout = timeout


class BitrixResponseError(BitrixSDKException, HTTPResponse):
    """
    Base class for errors raised when an HTTP response is received
    but indicates a failure.

    This exception wraps the original `requests.Response` object,
    allowing callers to inspect the full response.

    Parameters
    ----------
    message : Text
        Human-readable error message.
    response : requests.Response
        The HTTP response returned by the server.

    Attributes
    ----------
    response : requests.Response
        Original HTTP response object.
    """

    __slots__ = ("response",)

    def __init__(self, message: typing.Text, response: requests.Response):
        super().__init__(message, response)
        self.response = response


class BitrixResponseJSONDecodeError(BitrixResponseError):
    """
    Raised when the API response body cannot be parsed as JSON.

    This typically indicates that the server returned an unexpected
    response format (HTML, empty body, proxy error page, etc.).
    """

    __slots__ = ()

    def __init__(self, response: requests.Response):
        message = f"{self.__class__.__name__}: failed to decode {response}"
        super().__init__(message, response)


class BitrixResponse302JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseFound):
    """
    Raised when a 302 redirect response is returned instead of JSON.

    This may occur when the Bitrix portal domain has changed
    or the request was redirected to another endpoint.

    Properties
    ----------
    redirect_url : Optional[Text]
        Redirect target from the Location header.

    new_domain : Optional[Text]
        Extracted domain from the redirect URL.
    """

    __slots__ = ()

    @property
    def redirect_url(self) -> typing.Optional[typing.Text]:
        """Return redirect URL from the HTTP Location header."""
        return self.response.headers.get("Location")

    @property
    def new_domain(self) -> typing.Optional[typing.Text]:
        """
        Extract the hostname from the redirect URL.

        Returns
        -------
        Optional[Text]
            Redirected portal domain if available.
        """
        redirect_url = self.redirect_url
        return redirect_url and _urlparse(redirect_url).hostname


class BitrixResponse403JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseForbidden):
    """
    Raised when a 403 Forbidden response cannot be parsed as JSON.

    Typically, indicates access restrictions or an HTML error page
    returned instead of the expected JSON payload.
    """

    __slots__ = ()


class BitrixResponse500JSONDecodeError(BitrixResponseJSONDecodeError, HTTPResponseInternalServerError):
    """
    Raised when a 500 Internal Server Error response cannot be parsed as JSON.

    Usually indicates that the server returned a non-JSON body while
    processing the request failed on the Bitrix side.
    """

    __slots__ = ()


class BaseBitrixAPIError(BitrixResponseError):
    """
    Base class for Bitrix API errors represented by a JSON response body.

    Raised when the Bitrix server returns an error payload in JSON format.
    The exact schema of the payload is not guaranteed to be stable and may
    differ across API versions, endpoints, and platform components.

    This class stores the raw parsed JSON response in `json_response`
    without enforcing a specific error response structure.

    Parameters
    ----------
    json_response : Dict
        Parsed JSON body returned by the API.
    response : requests.Response
        Original HTTP response object.

    Attributes
    ----------
    json_response : Dict
        Raw parsed JSON error payload.
    """

    __slots__ = ("json_response",)

    json_response: "_types.JSONDict"

    def __init__(self, json_response: "_types.JSONDict", response: requests.Response):
        error = json_response.get("error")

        if isinstance(error, dict):
            message = error.get("message", f"{self.__class__.__name__}: {response.text}")
        else:
            message = json_response.get("error_description", f"{self.__class__.__name__}: {response.text}")

        super().__init__(message, response)

        self.json_response = json_response


# ------------------------ Exceptions for API v1 and v2 ------------------------


class BitrixAPIError(BaseBitrixAPIError):
    """
    Base class for Bitrix REST API errors identified by a string error code.

    This class represents API errors returned in the legacy Bitrix REST
    error format (commonly used in earlier API versions), where the
    response payload contains fields such as:

        {
            "error": "...",
            "error_description": "...",
        }

    Subclasses correspond to specific Bitrix error codes and are usually
    associated with particular HTTP status codes.
    """

    ERROR: typing.ClassVar[typing.Text] = NotImplemented

    __slots__ = ()

    @property
    def error(self) -> typing.Text:
        """
        Return the Bitrix API error code.

        Returns
        -------
        Text
            Value of the `error` field in the API response.
        """
        return self.json_response.get("error") or ""

    @property
    def error_description(self) -> typing.Text:
        """
        Return the error description provided by the API.

        Returns
        -------
        Text
            Value of the `error_description` field.
        """
        return self.json_response.get("error_description") or ""


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError, HTTPResponseBadRequest):
    """Bad Request (400)."""

    __slots__ = ()


class BitrixAPIUnauthorized(BitrixAPIError, HTTPResponseUnauthorized):
    """Unauthorized (401)."""

    __slots__ = ()


class BitrixAPIForbidden(BitrixAPIError, HTTPResponseForbidden):
    """Forbidden (403)."""

    __slots__ = ()


class BitrixAPINotFound(BitrixAPIError, HTTPResponseNotFound):
    """Not Found (404).

    Raised when the specified resource cannot be located on the server.
    """

    __slots__ = ()


class BitrixAPIMethodNotAllowed(BitrixAPIError, HTTPResponseMethodNotAllowed):
    """Method Not Allowed (405).

    Indicates that the HTTP method used in the request is not allowed for the requested resource.
    """

    __slots__ = ()


class BitrixAPIGone(BitrixAPIError, HTTPResponseGone):
    """Gone (410)."""

    __slots__ = ()


class BitrixAPITooManyRequests(BitrixAPIError, HTTPResponseTooManyRequests):
    """Too Many Requests (429)."""

    __slots__ = ()


class BitrixAPIInternalServerError(BitrixAPIError, HTTPResponseInternalServerError):
    """Internal server error (500)."""

    __slots__ = ()


class BitrixAPIServiceUnavailable(BitrixAPIError, HTTPResponseServiceUnavailable):
    """Service Unavailable (503).

    Raised when the API service is temporarily unavailable, often due to maintenance or server overload.
    """

    __slots__ = ()


# Exceptions by error

# 400

class BitrixAPIInvalidArgValue(BitrixAPIBadRequest):
    """Invalid argument value provided.

    Raised when one or more request parameters contain values that
    cannot be processed by the API.
    """

    ERROR = "INVALID_ARG_VALUE"

    __slots__ = ()


class BitrixAPIInvalidRequest(BitrixAPIBadRequest):
    """Invalid request format.

    Indicates the request was incorrectly formed. In some cases this
    error occurs when the request is made over HTTP instead of HTTPS.
    """

    ERROR = "INVALID_REQUEST"

    __slots__ = ()


# 401

class BitrixAPIAuthorizationError(BitrixAPIUnauthorized):
    """User authorization failed.

    Typically, occurs when the Bitrix24 user associated with the token
    has been deactivated or removed.

    Example
    -------
    {
        "error": "authorization_error",
        "error_description": "Unable to authorize user",
    }
    """

    ERROR = "AUTHORIZATION_ERROR"

    __slots__ = ()


class BitrixAPIApplicationNotFound(BitrixAPIUnauthorized):
    """Application not found on the portal.

    Returned when a cached OAuth token references an application
    that has been deleted from the portal.

    Example
    -------
    {
        "error": "APPLICATION_NOT_FOUND",
        "error_description": "Application not found",
    }
    """

    ERROR = "APPLICATION_NOT_FOUND"

    __slots__ = ()


class BitrixAPIErrorOAuth(BitrixAPIUnauthorized):
    """OAuth application is not installed.

    Returned when the portal asks the OAuth server to validate the token
    and the application is no longer installed.

    Example
    -------
    {
        "error": "ERROR_OAUTH",
        "error_description": "Application not installed",
    }
    """

    ERROR = "ERROR_OAUTH"

    __slots__ = ()


class BitrixAPIExpiredToken(BitrixAPIUnauthorized):
    """
    Raised when the OAuth access token has expired.

    The client must refresh the token using the refresh_token.

    Example
    ----------------
    {
        "error": "expired_token",
        "error_description": "The access token provided has expired.",
    }
    """

    ERROR = "EXPIRED_TOKEN"

    __slots__ = ()


class BitrixAPIInsufficientScope(BitrixAPIUnauthorized):
    """Insufficient access scope.

    Raised when the current token does not provide enough permissions
    to execute the requested API method.

    Examples
    ----------------
    {
        "error": "insufficient_scope",
        "error_description": "The request requires higher privileges than provided by the access token",
    }

    {
        "error": "insufficient_scope",
        "error_description": "The request requires higher privileges than provided by the webhook token",
    }
    """

    ERROR = "INSUFFICIENT_SCOPE"

    __slots__ = ()


class BitrixAPIInvalidCredentials(BitrixAPIUnauthorized):
    """Invalid request credentials.

    Usually returned when a webhook token or authentication data
    is incorrect.

    Example
    -------
    {
        "error": "INVALID_CREDENTIALS",
        "error_description": "Invalid request credentials",
    }
    """

    ERROR = "INVALID_CREDENTIALS"

    __slots__ = ()


class BitrixAPIInvalidToken(BitrixAPIUnauthorized):
    """Invalid OAuth token.

    Raised when Bitrix cannot identify an application associated
    with the provided access token.

    Example
    -------
    {
        "error": "invalid_token",
        "error_description": "Unable to get application by token",
    }
    """

    ERROR = "INVALID_TOKEN"

    __slots__ = ()


class BitrixAPIMethodConfirmWaiting(BitrixAPIUnauthorized):
    """Waiting for user confirmation.

    Raised when a method requires user confirmation and the action
    has not yet been approved.

    Example
    -------
    {
        "error": "METHOD_CONFIRM_WAITING",
        "error_description": "Waiting for confirmation",
    }
    """

    ERROR = "METHOD_CONFIRM_WAITING"

    __slots__ = ()


class BitrixAPINoAuthFound(BitrixAPIUnauthorized):
    """Authorization data was not found in the request.

    Raised when no valid authentication credentials are present.

    Example
    -------
    {
        "error": "NO_AUTH_FOUND",
        "error_description": "Wrong authorization data",
    }
    """

    ERROR = "NO_AUTH_FOUND"

    __slots__ = ()


class BitrixAPIPaymentRequired(BitrixAPIUnauthorized):
    """Portal subscription has expired.

    Returned when the Bitrix24 portal no longer has an active subscription.

    Example
    -------
    {
        "error": "PAYMENT_REQUIRED",
        "error_description": "Subscription has been ended",
    }
    """

    ERROR = "PAYMENT_REQUIRED"

    __slots__ = ()


# 403

class BitrixAPIAccessDenied(BitrixAPIForbidden):
    """REST API access is restricted.

    Typically, returned when the REST API is only available
    on commercial Bitrix24 plans.

    Examples
    -------
    {
        "error": "ACCESS_DENIED",
        "error_description": "Access denied!",
    }

    {
        "error": "ACCESS_DENIED",
        "error_description": "Access denied! Available only on extended plans",
    }

    {
        "error": "ACCESS_DENIED",
        "error_description": "Current user can't be authorized in this context",
    }

    {
        "error": "ACCESS_DENIED",
        "error_description": "REST is available only on commercial plans.",
    }
    """

    ERROR = "ACCESS_DENIED"

    __slots__ = ()


class BitrixAPIAllowedOnlyIntranetUser(BitrixAPIForbidden):
    """Method is allowed only for intranet users."""

    ERROR = "ALLOWED_ONLY_INTRANET_USER"

    __slots__ = ()


class BitrixAPIMethodConfirmDenied(BitrixAPIForbidden):
    """User denied confirmation for the requested method."""

    ERROR = "METHOD_CONFIRM_DENIED"

    __slots__ = ()


class BitrixAPIUserAccessError(BitrixAPIForbidden):
    """User does not have access to the application.

    Example
    -------
    {
        "error": "user_access_error",
        "error_description": "The user does not have access to the application.",
    }
    """

    ERROR = "USER_ACCESS_ERROR"

    __slots__ = ()


class BitrixAPIWrongAuthType(BitrixAPIForbidden):
    """Current authorization type is not allowed for this method."""

    ERROR = "WRONG_AUTH_TYPE"

    __slots__ = ()


# 410

class BitrixAPIPortalDeleted(BitrixAPIGone):
    """Portal has been deleted.

    Example
    -------
    {
        "error": "PORTAL_DELETED",
        "error_description": "Portal was deleted",
    }
    """

    ERROR = "PORTAL_DELETED"

    __slots__ = ()


# 429

class BitrixAPIOperationTimeLimit(BitrixAPITooManyRequests):
    """Method execution time limit exceeded.

    The request was blocked because the operation exceeded
    the allowed execution time.

    Example
    -------
    {
        "error": "OPERATION_TIME_LIMIT",
        "error_description": "Method is blocked due to operation time limit.",
    }
    """

    ERROR = "OPERATION_TIME_LIMIT"

    __slots__ = ()


# 500

class BitrixAPIErrorUnexpectedAnswer(BitrixAPIInternalServerError):
    """Server returned an unexpected response.

    Raised when the API response does not match the expected
    format or structure.

    Example
    -------
    {
        "error": "ERROR_UNEXPECTED_ANSWER",
        "error_description": "Server returned an unexpected response.",
    }
    """

    ERROR = "ERROR_UNEXPECTED_ANSWER"

    __slots__ = ()


# 503

class BitrixAPIOverloadLimit(BitrixAPIServiceUnavailable):
    """REST API temporarily blocked due to server overload.

    Example
    -------
    {
        "error": "OVERLOAD_LIMIT",
        "error_description": "REST API is blocked due to overload.",
    }
    """

    ERROR = "OVERLOAD_LIMIT"

    __slots__ = ()


class BitrixAPIQueryLimitExceeded(BitrixAPIServiceUnavailable):
    """Too many API requests were sent.

    Indicates that the request rate exceeded the allowed limit
    and the client should reduce the request frequency.

    Example
    -------
    {
        "error": "QUERY_LIMIT_EXCEEDED",
        "error_description": "Too many requests",
    }
    """

    ERROR = "QUERY_LIMIT_EXCEEDED"

    __slots__ = ()
