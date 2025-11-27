from typing import Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.events,
]

_SCOPE: Text = "crm"


@pytest.mark.oauth_only
def test_events(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.events(scope=_SCOPE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    events = cast(list, bitrix_response.result)

    assert len(events) > 0, "Events list should not be empty"

    for event in events:
        assert isinstance(event, str), "Event should be a string"
        assert event.startswith(f"ON{_SCOPE}".upper()), f"Event should be prefixed with ON{_SCOPE!r}"


@pytest.mark.oauth_only
def test_events_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.events(full=True).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    events = cast(list, bitrix_response.result)

    assert len(events) > 0, "Events list should not be empty"

    for event in events:
        assert isinstance(event, str), "Event should be a string"
