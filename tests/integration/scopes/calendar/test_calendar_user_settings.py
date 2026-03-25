from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_user_settings,
]

_USER_SETTINGS_FIELDS: Tuple[Text, ...] = ("view", "showDeclined", "showTasks", "timezoneName")


def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.calendar.user.settings.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "calendar.user.settings.get result should be a dict"

    settings = bitrix_response.result
    for field in _USER_SETTINGS_FIELDS:
        assert field in settings, f"Field '{field}' should be present"


def test_set(bitrix_client: BaseClient):
    """"""

    current_response = bitrix_client.calendar.user.settings.get().response

    assert isinstance(current_response, BitrixAPIResponse)
    assert isinstance(current_response.result, dict), "calendar.user.settings.get result should be a dict"

    current_settings = current_response.result
    for field in _USER_SETTINGS_FIELDS:
        assert field in current_settings, f"Field '{field}' should be present"

    bitrix_response = bitrix_client.calendar.user.settings.set(settings=current_settings).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.user.settings.set result should be bool"
    assert bitrix_response.result is True, "calendar.user.settings.set should return True"
