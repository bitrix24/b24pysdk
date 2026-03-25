import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_SEARCH_ITEM_FIELDS = (
    "id",
    "name",
)

_LAST_ITEM_FIELDS = (
    "id",
    "type",
)


def _dialog_id() -> str:
    return str(BITRIX_PORTAL_OWNER_ID)


def test_search_chat_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.search.chat.list(find=SDK_NAME, limit=10).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.search.chat.list result should be a list"

    for chat in bitrix_response.result:
        assert isinstance(chat, dict), "Each chat should be a dict"
        for field in _SEARCH_ITEM_FIELDS:
            assert field in chat, f"Field '{field}' should be present"


def test_search_department_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.search.department.list(find=SDK_NAME, limit=10).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.search.department.list result should be a list"


def test_search_user_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.search.user.list(find=SDK_NAME, limit=10).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.search.user.list result should be a list"


def test_search_last_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.search.last.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.search.last.get result should be a list"

    for item in bitrix_response.result:
        assert isinstance(item, dict), "Each last search item should be a dict"
        for field in _LAST_ITEM_FIELDS:
            assert field in item, f"Field '{field}' should be present"


def test_search_last_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.search.last.add(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.search.last.add result should be bool"


def test_search_last_delete(bitrix_client: BaseClient):
    """"""

    _ = bitrix_client.im.search.last.add(dialog_id=_dialog_id()).response
    bitrix_response = bitrix_client.im.search.last.delete(dialog_id=_dialog_id()).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.search.last.delete result should be bool"
