from . import BitrixAPIBadRequest as _BitrixAPIBadRequest
from . import BitrixAPIError as _BitrixAPIError
from . import BitrixAPIForbidden as _BitrixAPIForbidden
from . import BitrixAPIInsufficientScope as _BitrixAPIInsufficientScope
from . import BitrixAPIInvalidRequest as _BitrixAPIInvalidRequest
from . import BitrixAPIUnauthorized as _BitrixAPIUnauthorized
from . import BitrixRequestError as _BitrixRequestError
from . import BitrixRequestTimeout as _BitrixRequestTimeout
from . import BitrixSDKException as _BitrixSDKException
from ._http_responses import HTTPResponseOK

__all__ = [
    "BitrixOAuthException",
    "BitrixOAuthInsufficientScope",
    "BitrixOAuthInvalidClient",
    "BitrixOAuthInvalidGrant",
    "BitrixOAuthInvalidRequest",
    "BitrixOAuthInvalidScope",
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

class BitrixOauthWrongClient(_BitrixAPIError, BitrixOAuthException, HTTPResponseOK):
    """OAuth client credentials are invalid."""

    ERROR = "WRONG_CLIENT"

    __slots__ = ()


# 400

class BitrixOAuthInvalidClient(_BitrixAPIBadRequest, BitrixOAuthException):
    """Invalid OAuth client credentials."""

    ERROR = "INVALID_CLIENT"

    __slots__ = ()


class BitrixOAuthInvalidGrant(_BitrixAPIBadRequest, BitrixOAuthException):
    """
    Invalid OAuth authorization grant.

    Typically returned by `/oauth/token/` when the provided
    authorization code or refresh token is invalid, expired,
    revoked, or already used.
    """

    ERROR = "INVALID_GRANT"

    __slots__ = ()


class BitrixOAuthInvalidRequest(_BitrixAPIInvalidRequest, BitrixOAuthException):
    """Invalid OAuth authorization request."""

    __slots__ = ()


# 401

class BitrixOAuthNotInstalled(_BitrixAPIUnauthorized, BitrixOAuthException):
    """Application is not installed on the portal."""

    ERROR = "NOT_INSTALLED"

    __slots__ = ()


# 403

class BitrixOAuthInsufficientScope(_BitrixAPIInsufficientScope, BitrixOAuthException):
    """OAuth token does not provide sufficient permissions."""

    __slots__ = ()


class BitrixOAuthInvalidScope(_BitrixAPIForbidden, BitrixOAuthException):
    """Requested OAuth scope exceeds application permissions."""

    ERROR = "INVALID_SCOPE"

    __slots__ = ()
