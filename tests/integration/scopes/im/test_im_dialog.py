import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_DIALOG_FIELDS = (
    "dialog_id",
    "name",
    "type",
)


def _dialog_id() -> str:
    return str(BITRIX_PORTAL_OWNER_ID)


def test_dialog_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.dialog.get(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.dialog.get result should be a dict"

    dialog_data = bitrix_response.result

    for field in _DIALOG_FIELDS:
        assert field in dialog_data, f"Field '{field}' should be present"


def test_dialog_writing(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.dialog.writing(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.dialog.writing result should be bool"


def test_dialog_messages_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.dialog.messages.get(dialog_id=_dialog_id(), limit=10).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.dialog.messages.get result should be a dict"


def test_dialog_users_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.dialog.users.list(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.dialog.users.list result should be a list"


def test_dialog_read_all(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.dialog.read.all().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.dialog.read.all result should be bool"


def test_dialog_read(bitrix_client: BaseClient):
    """"""

    message_id_response = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.dialog.read").response
    assert isinstance(message_id_response, BitrixAPIResponse)
    assert isinstance(message_id_response.result, int), "im.message.add should return message id"

    bitrix_response = bitrix_client.im.dialog.read(dialog_id=_dialog_id(), message_id=message_id_response.result).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (dict, bool)), "im.dialog.read result should be dict or bool"
    if isinstance(bitrix_response.result, dict):
        assert len(bitrix_response.result) > 0, "im.dialog.read result dict should not be empty"


def test_dialog_unread(bitrix_client: BaseClient):
    """"""

    message_id_response = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.dialog.unread").response
    assert isinstance(message_id_response, BitrixAPIResponse)
    assert isinstance(message_id_response.result, int), "im.message.add should return message id"

    bitrix_response = bitrix_client.im.dialog.unread(
        dialog_id=_dialog_id(),
        message_id=message_id_response.result,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.dialog.unread result should be bool"


def test_dialog_messages_search(bitrix_client: BaseClient):
    """"""

    chat_id_response = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT", message=f"{SDK_NAME} search").response
    assert isinstance(chat_id_response, BitrixAPIResponse)
    assert isinstance(chat_id_response.result, int), "im.chat.add should return chat id"

    bitrix_response = bitrix_client.im.dialog.messages.search(chat_id=chat_id_response.result, limit=10).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.dialog.messages.search result should be a dict"
