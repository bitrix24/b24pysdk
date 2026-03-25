from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_settings,
]

_SETTINGS_FIELDS: Tuple[Text, ...] = ("work_time_start", "work_time_end", "week_start", "week_holidays")


def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.calendar.settings.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "calendar.settings.get result should be a dict"

    settings = bitrix_response.result
    for field in _SETTINGS_FIELDS:
        assert field in settings, f"Field '{field}' should be present"
