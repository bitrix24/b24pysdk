from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pytest
import requests

from b24pysdk.api.requesters._utils.parse_response import parse_response
from b24pysdk.credentials import BitrixApp, BitrixToken
from b24pysdk.errors.oauth import (
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidClient,
    BitrixOAuthInvalidGrant,
    BitrixOAuthInvalidRequest,
    BitrixOAuthInvalidScope,
    BitrixOAuthNoAuthFound,
    BitrixOAuthNotInstalled,
    BitrixOAuthRequestError,
    BitrixOAuthRequestTimeout,
    BitrixOauthWrongClient,
)
from tests.env_config import EnvConfig

if TYPE_CHECKING:
    from b24pysdk.errors import BitrixAPIError

pytestmark = [
    pytest.mark.integration,
    pytest.mark.errors,
    pytest.mark.errors_oauth,
]

env_config: EnvConfig = EnvConfig()
_TINY_TIMEOUT: float = 0.0001
_INVALID_REFRESH_TOKEN: str = "invalid_refresh_token"  # noqa: S105
_REST_BASE_URL = f"https://{env_config.domain}/rest"
_JSON_HEADERS = {"Accept": "application/json"}
_REQUEST_TIMEOUT = 10
_TEST_ENTITY_TYPE_ID = 1268
_TEST_ITEM_ID = 1


def _assert_error_response(exc: BitrixAPIError, error_cls: Type[BitrixAPIError]):
    assert exc.status_code == error_cls.STATUS_CODE

    expected_error = getattr(error_cls, "ERROR", NotImplemented)
    if exc.error and expected_error is not NotImplemented:
        assert exc.error.upper() == expected_error


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
    """Expect INVALID_CLIENT with wrong client_secret."""

    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret="WRONG_SECRET_12345",  # noqa: S106
    )

    with pytest.raises(BitrixOAuthInvalidClient) as exc_info:
        _ = bitrix_app.get_oauth_token(code="any_valid_or_invalid_code")

    _assert_error_response(exc_info.value, BitrixOAuthInvalidClient)


def test_error_bitrix_oauth_invalid_grant_refresh_token():
    """Expect INVALID_GRANT when refreshing with a wrong refresh_token."""

    bitrix_token = _make_refreshable_token(_INVALID_REFRESH_TOKEN)

    with pytest.raises(BitrixOAuthInvalidGrant) as exc_info:
        _ = bitrix_token.refresh_oauth_token()

    _assert_error_response(exc_info.value, BitrixOAuthInvalidGrant)


def test_error_bitrix_api_no_auth_found():
    """Expect BitrixAPINoAuthFound when auth is missing in the request (works)."""

    deleting_result = requests.post(
        f"{_REST_BASE_URL}/crm.item.delete",
        json={"entityTypeId": _TEST_ENTITY_TYPE_ID, "id": _TEST_ITEM_ID},
        headers=_JSON_HEADERS,
        timeout=_REQUEST_TIMEOUT,
    )

    with pytest.raises(BitrixOAuthNoAuthFound) as exc_info:
        parse_response(deleting_result)

    _assert_error_response(exc_info.value, BitrixOAuthNoAuthFound)


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
    """Expect WRONG_CLIENT with wrong client_id."""

    bitrix_app = BitrixApp(
        client_id="WRONG_CLIENT_ID_12345",
        client_secret=env_config.client_secret,
    )

    with pytest.raises(BitrixOauthWrongClient) as exc_info:
        _ = bitrix_app.get_oauth_token(code="any_code")

    _assert_error_response(exc_info.value, BitrixOauthWrongClient)
