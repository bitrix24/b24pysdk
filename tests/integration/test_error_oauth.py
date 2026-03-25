from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pytest

from b24pysdk.credentials import BitrixApp, BitrixToken
from b24pysdk.errors.oauth import (
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidClient,
    BitrixOAuthInvalidGrant,
    BitrixOAuthInvalidRequest,
    BitrixOAuthInvalidScope,
    BitrixOAuthNotInstalled,
    BitrixOAuthRequestError,
    BitrixOAuthRequestTimeout,
    BitrixOauthWrongClient,
)
from tests.constants import DELETED_APP_REFRESH_TOKEN
from tests.env_config import EnvConfig

if TYPE_CHECKING:
    from b24pysdk.errors import BitrixAPIError

pytestmark = [
    pytest.mark.integration,
    pytest.mark.test_error,
]

env_config: EnvConfig = EnvConfig()
_TINY_TIMEOUT: float = 0.0001
_INVALID_REFRESH_TOKEN: str = "invalid_refresh_token"  # noqa: S105


def _assert_error_response(exc: BitrixAPIError, error_cls: Type[BitrixAPIError]):
    assert exc.status_code == error_cls.STATUS_CODE

    expected_error = getattr(error_cls, "ERROR", NotImplemented)
    if exc.error and expected_error is not NotImplemented:
        assert exc.error.upper() == expected_error


def _require_oauth_app_credentials():
    if not env_config.domain or not env_config.client_id or not env_config.client_secret:
        pytest.skip("Missing OAuth app credentials: B24_DOMAIN, B24_CLIENT_ID, B24_CLIENT_SECRET")


def _make_refreshable_token(refresh_token: str) -> BitrixToken:
    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )
    return BitrixToken(
        domain=env_config.domain,
        auth_token="EXPIRED_TOKEN_FOR_REFRESH_FLOW",  # noqa: S106
        refresh_token=refresh_token,
        bitrix_app=bitrix_app,
    )


def test_error_bitrix_oauth_request_timeout():
    """Expect BitrixOAuthRequestTimeout with an unrealistically small timeout."""
    if not env_config.are_oauth_credentials_available:
        pytest.skip("Missing OAuth credentials")

    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )

    with pytest.raises(BitrixOAuthRequestTimeout) as exc_info:
        _ = bitrix_app.get_oauth_token(code="any_code", timeout=_TINY_TIMEOUT, max_retries=1)

    assert exc_info.value.timeout == _TINY_TIMEOUT


def test_error_bitrix_oauth_invalid_client():
    """Expect INVALID_CLIENT when using wrong OAuth client credentials (works)."""
    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret="WRONG_SECRET_12345",  # noqa: S106
    )

    with pytest.raises(BitrixOAuthInvalidClient) as exc_info:
        _ = bitrix_app.get_oauth_token(code="any_valid_or_invalid_code")

    _assert_error_response(exc_info.value, BitrixOAuthInvalidClient)


def test_error_bitrix_oauth_invalid_grant():
    """Expect INVALID_GRANT when reusing/invalidating an auth code or refresh token (works)."""
    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )

    with pytest.raises(BitrixOAuthInvalidGrant) as exc_info:
        _ = bitrix_app.get_oauth_token(code=env_config.access_token)

    _assert_error_response(exc_info.value, BitrixOAuthInvalidGrant)


def test_error_bitrix_oauth_invalid_grant_refresh_token():
    """Expect INVALID_GRANT when refreshing with a wrong refresh_token."""
    _require_oauth_app_credentials()

    bitrix_token = _make_refreshable_token(_INVALID_REFRESH_TOKEN)

    with pytest.raises(BitrixOAuthInvalidGrant) as exc_info:
        _ = bitrix_token.refresh_oauth_token()

    _assert_error_response(exc_info.value, BitrixOAuthInvalidGrant)


def test_error_bitrix_oauth_insufficient_scope():
    """Could not reproduce OAuth insufficient_scope; left skipped."""
    pytest.skip(BitrixOAuthInsufficientScope.__name__)


def test_error_bitrix_oauth_invalid_request():
    """OAuth INVALID_REQUEST is not reproducible in stable CI conditions."""
    pytest.skip(BitrixOAuthInvalidRequest.__name__)


def test_error_bitrix_oauth_invalid_scope():
    """OAuth INVALID_SCOPE requires app scope mismatch setup."""
    pytest.skip(BitrixOAuthInvalidScope.__name__)


def test_error_bitrix_oauth_not_installed():
    """OAuth NOT_INSTALLED requires dedicated app uninstall scenario."""
    pytest.skip(BitrixOAuthNotInstalled.__name__)


def test_error_bitrix_oauth_request_error():
    """OAuth request transport error is environment-dependent."""
    pytest.skip(BitrixOAuthRequestError.__name__)


def test_error_bitrix_oauth_wrong_client():
    """WRONG_CLIENT on refresh for a deleted app.

    How to obtain token:
    1. Install app on a test portal and complete OAuth once.
    2. Save the issued refresh token.
    3. Completely delete the app (not only disable scopes).
    4. Use saved refresh token in this test as DELETED_APP_REFRESH_TOKEN.
    """
    _require_oauth_app_credentials()

    if not DELETED_APP_REFRESH_TOKEN:
        pytest.skip("Set DELETED_APP_REFRESH_TOKEN to run WRONG_CLIENT refresh scenario")

    bitrix_token = _make_refreshable_token(DELETED_APP_REFRESH_TOKEN)

    with pytest.raises(BitrixOauthWrongClient) as exc_info:
        _ = bitrix_token.refresh_oauth_token()

    _assert_error_response(exc_info.value, BitrixOauthWrongClient)
