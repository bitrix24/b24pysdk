from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAppInfoResponse
from b24pysdk.client import BaseClient
from b24pysdk.credentials import BitrixToken
from b24pysdk.credentials.auth import RenewedOAuth
from b24pysdk.errors.oauth import BitrixOAuthInvalidGrant

pytestmark = [
    pytest.mark.integration,
    pytest.mark.credentials,
    pytest.mark.bitrix_token_integration,
]

_INVALID_CODE: Text = "invalid_oauth_code_for_test"


def _get_oauth_token(bitrix_client: BaseClient) -> BitrixToken:
    bitrix_token = bitrix_client._bitrix_token
    assert isinstance(bitrix_token, BitrixToken), "OAuth client should use BitrixToken"
    return bitrix_token


@pytest.mark.oauth_only
def test_bitrix_token_get_oauth_token(bitrix_client: BaseClient):
    """"""

    bitrix_token = _get_oauth_token(bitrix_client)

    with pytest.raises(BitrixOAuthInvalidGrant):
        _ = bitrix_token.get_oauth_token(_INVALID_CODE)


@pytest.mark.oauth_only
def test_bitrix_token_refresh_oauth_token(bitrix_client: BaseClient):
    """"""

    bitrix_token = _get_oauth_token(bitrix_client)

    renewed_oauth = bitrix_token.refresh_oauth_token()

    assert isinstance(renewed_oauth, RenewedOAuth)
    assert isinstance(renewed_oauth.oauth_token.access_token, str)
    assert len(renewed_oauth.oauth_token.access_token) > 0
    assert isinstance(renewed_oauth.oauth_token.refresh_token, str)
    assert len(renewed_oauth.oauth_token.refresh_token) > 0


@pytest.mark.oauth_only
def test_bitrix_token_get_app_info(bitrix_client: BaseClient):
    """"""

    bitrix_token = _get_oauth_token(bitrix_client)

    bitrix_response = bitrix_token.get_app_info()

    assert isinstance(bitrix_response, BitrixAppInfoResponse)
    assert isinstance(bitrix_response.result.client_id, str)
    assert len(bitrix_response.result.client_id) > 0
