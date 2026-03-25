import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]


def test_chat_user_add(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.user.add(chat_id=chat_id, users=[BITRIX_PORTAL_OWNER_ID]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.user.add result should be bool"


def test_chat_user_list(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.user.list(chat_id=chat_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.chat.user.list result should be a list"


def test_chat_user_delete(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.user.delete(chat_id=chat_id, user_id=BITRIX_PORTAL_OWNER_ID).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.user.delete result should be bool"
