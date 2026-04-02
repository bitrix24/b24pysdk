from . import BitrixAPIBadRequest as _BitrixAPIBadRequest
from . import BitrixAPIError as _BitrixAPIError
from . import BitrixAPIForbidden as _BitrixAPIForbidden
from . import BitrixAPIInsufficientScope as _BitrixAPIInsufficientScope
from . import BitrixAPIInvalidRequest as _BitrixAPIInvalidRequest
from . import BitrixAPIUnauthorized as _BitrixAPIUnauthorized
from . import BitrixRequestError as _BitrixRequestError
from . import BitrixRequestTimeout as _BitrixRequestTimeout
from . import BitrixSDKException as _BitrixSDKException
from ._http_responses import HTTPResponseOK as _HTTPResponseOK

__all__ = [
    "BitrixOAuthException",
    "BitrixOAuthInsufficientScope",
    "BitrixOAuthInvalidClient",
    "BitrixOAuthInvalidGrant",
    "BitrixOAuthInvalidRequest",
    "BitrixOAuthInvalidScope",
    "BitrixOAuthNoAuthFound",
    "BitrixOAuthNotInstalled",
    "BitrixOAuthRequestError",
    "BitrixOAuthRequestTimeout",
    "BitrixOauthWrongClient",
]


class BitrixOAuthException(_BitrixSDKException):
    """
    Base class for all OAuth-related errors.

    These errors occur during OAuth authentication flows,
    including authorization, token exchange, and scope validation.
    """

    __slots__ = ()


class BitrixOAuthRequestError(_BitrixRequestError, BitrixOAuthException):
    """An error occurred during an OAuth operation."""

    __slots__ = ()


class BitrixOAuthRequestTimeout(_BitrixRequestTimeout, BitrixOAuthException):
    """
    Raised when an OAuth HTTP request exceeds the configured timeout.

    Usually occurs during token exchange, refresh, or validation calls
    to the Bitrix OAuth endpoint.
    """

    __slots__ = ()


# Exceptions by error

# 200

class BitrixOauthWrongClient(_BitrixAPIError, BitrixOAuthException, _HTTPResponseOK):
    """OAuth app client_id is invalid.

    Example
    -------
    {
        "error": "wrong_client",
    }
    """

    ERROR = "WRONG_CLIENT"

    __slots__ = ()


# 400

class BitrixOAuthInvalidClient(_BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid OAuth client_secret.

    Also, can be returned by `/rest/app.info/` when access token is invalid
    but has token-like format.

    Example
    -------
    {
        "error": "invalid_client",
    }
    """

    ERROR = "INVALID_CLIENT"

    __slots__ = ()


class BitrixOAuthInvalidGrant(_BitrixAPIBadRequest, BitrixOAuthException):
    """
    Invalid OAuth refresh_token.

    Example
    -------
    {
        "error": "invalid_grant",
    }
    """

    ERROR = "INVALID_GRANT"

    __slots__ = ()


class BitrixOAuthInvalidRequest(_BitrixAPIInvalidRequest, BitrixOAuthException):
    """Invalid OAuth token refresh request.

    Returned when the `refresh_token` parameter is missing or empty.

    Example
    -------
    {
        "error": "invalid_request",
        "error_description": "No "refresh_token" parameter found",
    }
    """

    __slots__ = ()


# 401

class BitrixOAuthNoAuthFound(_BitrixAPIUnauthorized, BitrixOAuthException):
    """Wrong authorization data in OAuth-related context.

    Example
    -------
    {
        "error": "NO_AUTH_FOUND",
        "error_description": "Wrong authorization data",
    }
    """

    ERROR = "NO_AUTH_FOUND"

    __slots__ = ()


class BitrixOAuthNotInstalled(_BitrixAPIUnauthorized, BitrixOAuthException):
    """Application was removed from the portal.

    Example
    -------
    {
        "error": "NOT_INSTALLED",
        "error_description": "Application not installed",
    }
    """

    ERROR = "NOT_INSTALLED"

    __slots__ = ()


# 403

class BitrixOAuthInsufficientScope(_BitrixAPIInsufficientScope, BitrixOAuthException):
    """OAuth token does not provide sufficient permissions.

    Example
    -------
    {
        "error": "insufficient_scope",
        "error_description": "The request requires higher privileges than provided by the access token",
    }
    """

    __slots__ = ()


class BitrixOAuthInvalidScope(_BitrixAPIForbidden, BitrixOAuthException):
    """Requested OAuth scope exceeds application permissions.

    Example
    -------
    {
        "error": "INVALID_SCOPE",
        "error_description": "Given scope exceeds permissions associated with given grant",
    }
    """

    ERROR = "INVALID_SCOPE"

    __slots__ = ()
