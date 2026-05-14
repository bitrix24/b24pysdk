from unittest.mock import Mock, patch

import pytest

from b24pysdk.credentials import BitrixToken

pytestmark = [
    pytest.mark.unit,
    pytest.mark.credentials,
    pytest.mark.bitrix_token,
]

_DOMAIN = "test.bitrix24.ru"
_AUTH_TOKEN = "access_token_123"  # noqa: S105
_REFRESH_TOKEN = "refresh_token_123"  # noqa: S105
_CODE = "oauth_code_123"


def _make_token_with_app():
    bitrix_app = Mock()
    token = BitrixToken(
        domain=_DOMAIN,
        auth_token=_AUTH_TOKEN,
        refresh_token=_REFRESH_TOKEN,
        bitrix_app=bitrix_app,
    )
    return token, bitrix_app


@pytest.mark.parametrize(
    "call",
    [
        lambda token: token.get_oauth_token(_CODE),
        lambda token: token.refresh_oauth_token(),
        lambda token: token.get_app_info(),
    ],
)
def test_bitrix_token_oauth_methods_require_bitrix_app(call):
    token = BitrixToken(
        domain=_DOMAIN,
        auth_token=_AUTH_TOKEN,
        refresh_token=_REFRESH_TOKEN,
    )

    with pytest.raises(AttributeError):
        call(token)


def test_bitrix_token_get_oauth_token_delegates_to_bitrix_app():
    token, bitrix_app = _make_token_with_app()
    expected = Mock()
    bitrix_app.get_oauth_token.return_value = expected

    result = token.get_oauth_token(_CODE, timeout=3, max_retries=1)

    bitrix_app.get_oauth_token.assert_called_once_with(code=_CODE, timeout=3, max_retries=1)
    assert result is expected


def test_bitrix_token_refresh_oauth_token_delegates_with_refresh_token():
    token, bitrix_app = _make_token_with_app()
    expected = Mock()
    bitrix_app.refresh_oauth_token.return_value = expected

    result = token.refresh_oauth_token(timeout=5)

    bitrix_app.refresh_oauth_token.assert_called_once_with(refresh_token=_REFRESH_TOKEN, timeout=5)
    assert result is expected


def test_bitrix_token_get_app_info_uses_execute_with_retries():
    token, bitrix_app = _make_token_with_app()
    expected = Mock()
    bitrix_app.get_app_info.return_value = expected

    with patch.object(token, "_execute_with_retries", side_effect=lambda func: func()) as execute_mock:
        result = token.get_app_info(timeout=10)

    execute_mock.assert_called_once()
    bitrix_app.get_app_info.assert_called_once_with(_AUTH_TOKEN, timeout=10)
    assert result is expected
