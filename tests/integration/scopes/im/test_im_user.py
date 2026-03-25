import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_STATUS: str = "online"
_USER_FIELDS = ("id", "name", "last_name")
_STATUS_VALUES = ("online", "dnd", "away", "break")


def test_user_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.user.get(bitrix_id=BITRIX_PORTAL_OWNER_ID).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.user.get result should be a dict"

    user_data = bitrix_response.result

    for field in _USER_FIELDS:
        assert field in user_data, f"Field '{field}' should be present"


def test_user_list_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.user.list.get(bitrix_id=[BITRIX_PORTAL_OWNER_ID]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.user.list.get result should be a dict"

    users_data = bitrix_response.result

    for user_id, user_data in users_data.items():
        assert isinstance(user_id, str), "User id key should be a string"
        assert isinstance(user_data, dict), "Each user should be a dict"
        for field in _USER_FIELDS:
            assert field in user_data, f"Field '{field}' should be present"


def test_user_status_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.user.status.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (str, bool)), "im.user.status.get result should be string or bool"
    if isinstance(bitrix_response.result, str):
        assert bitrix_response.result in _STATUS_VALUES, "im.user.status.get returned unknown status"


def test_user_status_set(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.user.status.set(status=_STATUS).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.user.status.set result should be bool"


def test_user_status_idle_start(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.user.status.idle.start().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.user.status.idle.start result should be bool"


def test_user_status_idle_end(bitrix_client: BaseClient):
    """"""

    _ = bitrix_client.im.user.status.idle.start().response
    bitrix_response = bitrix_client.im.user.status.idle.end().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "im.user.status.idle.end result should be bool"
