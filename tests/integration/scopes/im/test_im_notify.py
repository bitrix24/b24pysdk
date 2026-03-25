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

_NOTIFY_GET_FIELDS = (
    "total_count",
    "total_unread_count",
    "chat_id",
    "notifications",
    "users",
)

_NOTIFY_HISTORY_FIELDS = (
    "notifications",
    "users",
)


def _new_tag() -> str:
    return f"sdk_im_notify_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"


def test_notify_call(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify",
        type="USER",
        tag=_new_tag(),
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "im.notify result should be notify id"


def test_notify_personal_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.personal.add",
        tag=_new_tag(),
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "im.notify.personal.add result should be notify id"


def test_notify_system_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.system.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.system.add",
        tag=_new_tag(),
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "im.notify.system.add result should be notify id"


def test_notify_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.get(limit=20).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.get result should be a dict"

    notifications_data = bitrix_response.result

    for field in _NOTIFY_GET_FIELDS:
        assert field in notifications_data, f"Field '{field}' should be present"


def test_notify_history_search(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.history.search(search_text=SDK_NAME, limit=20).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.history.search result should be a dict"

    history_data = bitrix_response.result

    for field in _NOTIFY_HISTORY_FIELDS:
        assert field in history_data, f"Field '{field}' should be present"


def test_notify_schema_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.schema.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.schema.get result should be a dict"
    assert len(bitrix_response.result) > 0, "im.notify.schema.get result should not be empty"


def test_notify_read_all(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.notify.read.all().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.read.all result should be a dict"


def test_notify_read(bitrix_client: BaseClient):
    """"""

    notify_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.read",
        tag=_new_tag(),
    ).response
    assert isinstance(notify_response, BitrixAPIResponse)
    assert isinstance(notify_response.result, int)

    bitrix_response = bitrix_client.im.notify.read(bitrix_id=notify_response.result).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.notify.read result should be bool"


def test_notify_read_list(bitrix_client: BaseClient):
    """"""

    notify_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.read.list",
        tag=_new_tag(),
    ).response
    assert isinstance(notify_response, BitrixAPIResponse)
    assert isinstance(notify_response.result, int)

    bitrix_response = bitrix_client.im.notify.read.list(ids=[notify_response.result], action=True).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.notify.read.list result should be bool"


def test_notify_delete(bitrix_client: BaseClient):
    """"""

    notify_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.delete",
        tag=_new_tag(),
    ).response
    assert isinstance(notify_response, BitrixAPIResponse)
    assert isinstance(notify_response.result, int), "im.notify.personal.add result should be notify id"

    bitrix_response = bitrix_client.im.notify.delete(bitrix_id=notify_response.result).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.notify.delete result should be bool"


def test_notify_answer(bitrix_client: BaseClient):
    """"""

    notify_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.answer",
        tag=_new_tag(),
    ).response
    assert isinstance(notify_response, BitrixAPIResponse)
    assert isinstance(notify_response.result, int)

    try:
        bitrix_response = bitrix_client.im.notify.answer(bitrix_id=notify_response.result, answer_text="OK").response
    except BitrixAPIError:
        return

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.answer result should be a dict"
    assert len(bitrix_response.result) > 0, "im.notify.answer result should not be empty"


def test_notify_confirm(bitrix_client: BaseClient):
    """"""

    notify_response = bitrix_client.im.notify.personal.add(
        user_id=BITRIX_PORTAL_OWNER_ID,
        message=f"{SDK_NAME} im.notify.confirm",
        tag=_new_tag(),
    ).response
    assert isinstance(notify_response, BitrixAPIResponse)
    assert isinstance(notify_response.result, int)

    try:
        bitrix_response = bitrix_client.im.notify.confirm(bitrix_id=notify_response.result, notify_value=True).response
    except BitrixAPIError:
        return

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.notify.confirm result should be a dict"
    assert len(bitrix_response.result) > 0, "im.notify.confirm result should not be empty"
