from datetime import timedelta
from typing import Text, Tuple

import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_accessibility,
]

_ACCESSIBILITY_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "DATE_FROM", "DATE_TO")


def test_get(bitrix_client: BaseClient):
    """"""

    from_date = Config().get_local_date().isoformat()
    to = (Config().get_local_date() + timedelta(days=7)).isoformat()

    bitrix_response = bitrix_client.calendar.accessibility.get(
        users=[BITRIX_PORTAL_OWNER_ID],
        from_date=from_date,
        to=to,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "calendar.accessibility.get result should be a dict"

    accessibility = bitrix_response.result
    user_key = str(BITRIX_PORTAL_OWNER_ID)
    assert user_key in accessibility, f"User key '{user_key}' should be present"
    assert isinstance(accessibility[user_key], list), "User accessibility value should be a list"

    for event in accessibility[user_key]:
        assert isinstance(event, dict), "Each accessibility event should be a dict"
        for field in _ACCESSIBILITY_FIELDS:
            assert field in event, f"Field '{field}' should be present"
