from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.sign,
    pytest.mark.sign_b2e,
]

_MYSAFE_ITEM_FIELDS: Tuple[Text, ...] = (
    "id",
    "title",
    "create_date",
    "signed_date",
    "creator_id",
    "member_id",
    "role",
    "file_url",
)
_PERSONAL_ITEM_FIELDS: Tuple[Text, ...] = (
    "id",
    "title",
    "signed_date",
    "file_url",
)


@pytest.mark.oauth_only
def test_mysafe_tail(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.sign.b2e.mysafe.tail(limit=1, offset=0).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "sign.b2e.mysafe.tail result should be a list"

    tail_items = bitrix_response.result
    for item in tail_items:
        assert isinstance(item, dict), "Each sign.b2e.mysafe.tail item should be a dict"
        for field in _MYSAFE_ITEM_FIELDS:
            assert field in item, f"Field '{field}' should be present"


@pytest.mark.oauth_only
def test_personal_tail(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.sign.b2e.personal.tail(limit=1, offset=0).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "sign.b2e.personal.tail result should be a list"

    tail_items = bitrix_response.result
    for item in tail_items:
        assert isinstance(item, dict), "Each sign.b2e.personal.tail item should be a dict"
        for field in _PERSONAL_ITEM_FIELDS:
            assert field in item, f"Field '{field}' should be present"
