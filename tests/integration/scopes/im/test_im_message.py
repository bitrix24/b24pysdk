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


def _dialog_id() -> str:
    return str(BITRIX_PORTAL_OWNER_ID)


def test_message_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.message.add(
        dialog_id=_dialog_id(),
        message=f"{SDK_NAME} im.message.add {int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "im.message.add should return message id"


def test_message_update(bitrix_client: BaseClient):
    """"""

    message_id = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.message.update").response.result
    assert isinstance(message_id, int)

    bitrix_response = bitrix_client.im.message.update(message_id=message_id, message=f"{SDK_NAME} updated").response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.message.update result should be bool"


def test_message_like(bitrix_client: BaseClient):
    """"""

    message_id = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.message.like").response.result
    assert isinstance(message_id, int)

    bitrix_response = bitrix_client.im.message.like(message_id=message_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.message.like result should be bool"


def test_message_share(bitrix_client: BaseClient):
    """"""

    message_id = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.message.share").response.result
    assert isinstance(message_id, int)

    try:
        bitrix_response = bitrix_client.im.message.share(message_id=message_id, dialog_id=_dialog_id(), type="MESSAGE").response
    except BitrixAPIError:
        return

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.message.share result should be bool"


def test_message_delete(bitrix_client: BaseClient):
    """"""

    message_id = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.message.delete").response.result
    assert isinstance(message_id, int)

    bitrix_response = bitrix_client.im.message.delete(message_id=message_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.message.delete result should be bool"


def test_message_command(bitrix_client: BaseClient):
    """"""

    message_id = bitrix_client.im.message.add(dialog_id=_dialog_id(), message=f"{SDK_NAME} im.message.command").response.result
    assert isinstance(message_id, int)

    with pytest.raises(BitrixAPIError):
        _ = bitrix_client.im.message.command(message_id=message_id, bot_id=0, command="help").response
