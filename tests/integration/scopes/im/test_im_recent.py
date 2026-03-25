import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_RECENT_ITEM_FIELDS = (
    "id",
    "type",
)

_RECENT_LIST_FIELDS = (
    "items",
)


def _dialog_id() -> str:
    return str(BITRIX_PORTAL_OWNER_ID)


def test_recent_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.recent.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.recent.get result should be a list"

    for dialog in bitrix_response.result:
        assert isinstance(dialog, dict), "Each recent dialog should be a dict"
        for field in _RECENT_ITEM_FIELDS:
            assert field in dialog, f"Field '{field}' should be present"


def test_recent_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.recent.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.recent.list result should be a dict"

    recent_data = bitrix_response.result

    for field in _RECENT_LIST_FIELDS:
        assert field in recent_data, f"Field '{field}' should be present"

    assert isinstance(recent_data["items"], list), "Field 'items' should be a list"


def test_recent_hide(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.recent.hide(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.recent.hide result should be bool"


def test_recent_pin(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.recent.pin(dialog_id=_dialog_id(), pin=True).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.recent.pin result should be bool"


def test_recent_unread(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.recent.unread(dialog_id=_dialog_id(), action=True).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.recent.unread result should be bool"
