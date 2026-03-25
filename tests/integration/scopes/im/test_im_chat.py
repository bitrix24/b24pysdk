import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_CHAT_GET_FIELDS = ("ID",)


def test_chat_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.chat.add(
        users=[BITRIX_PORTAL_OWNER_ID],
        type="CHAT",
        title=f"{SDK_NAME} IM CHAT {int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "im.chat.add result should be chat id"
    assert bitrix_response.result > 0, "im.chat.add should return positive chat id"


def test_chat_get(bitrix_client: BaseClient):
    """"""

    entity_id = f"sdk_im_entity_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    chat_add_response = bitrix_client.im.chat.add(
        users=[BITRIX_PORTAL_OWNER_ID],
        type="CHAT",
        entity_type="SDK_IM",
        entity_id=entity_id,
    ).response

    assert isinstance(chat_add_response, BitrixAPIResponse)
    assert isinstance(chat_add_response.result, int)

    bitrix_response = bitrix_client.im.chat.get(entity_type="SDK_IM", entity_id=entity_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.chat.get result should be a dict"

    chat_data = bitrix_response.result

    for field in _CHAT_GET_FIELDS:
        assert field in chat_data, f"Field '{field}' should be present"


def test_chat_mute(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.mute(chat_id=chat_id, mute=True).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.mute result should be bool"


def test_chat_set_owner(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.set_owner(chat_id=chat_id, user_id=BITRIX_PORTAL_OWNER_ID).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.set_owner result should be bool"


def test_chat_update_color(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.update_color(chat_id=chat_id, color="SAND").response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.update_color result should be bool"


def test_chat_update_title(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.update_title(
        chat_id=chat_id,
        title=f"{SDK_NAME} IM TITLE {int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.update_title result should be bool"


def test_chat_update_avatar(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    try:
        bitrix_response = bitrix_client.im.chat.update_avatar(chat_id=chat_id, avatar="").response
    except BitrixAPIError:
        return

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.update_avatar result should be bool"


def test_chat_leave(bitrix_client: BaseClient):
    """"""

    chat_id = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response.result
    assert isinstance(chat_id, int)

    bitrix_response = bitrix_client.im.chat.leave(chat_id=chat_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.chat.leave result should be bool"
