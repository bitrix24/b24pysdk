from typing import Generator, Optional, Text, Tuple

import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.utils.types import JSONDict

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.event,
    pytest.mark.event_offline,
]

_FIELDS: Tuple[Text, ...] = ("ID", "TIMESTAMP_X", "EVENT_NAME", "EVENT_DATA", "EVENT_ADDITIONAL", "MESSAGE_ID")
_LIMIT: int = 1
_CLEAR: bool = False
_PROCESS_ID_FIELD: Text = "process_id"
_EVENTS_FIELD: Text = "events"
_ERROR_MESSAGE_ID: int = 1


def _get_first_offline_event(bitrix_client: BaseClient) -> Optional[JSONDict]:
    """"""

    bitrix_response = bitrix_client.event.offline.get(limit=_LIMIT, clear=_CLEAR).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert _PROCESS_ID_FIELD in result, "Field 'process_id' should be present"
    assert _EVENTS_FIELD in result, "Field 'events' should be present"

    events = result[_EVENTS_FIELD]

    assert isinstance(events, list), "Field 'events' should be a list"

    if not events:
        return None

    event = events[0]

    assert isinstance(event, dict), "Event should be a dict"

    for field in _FIELDS:
        assert field in event, f"Field '{field}' should be present"

    return event


@pytest.mark.oauth_only
def test_event_offline_get(bitrix_client: BaseClient):
    """"""

    event = _get_first_offline_event(bitrix_client)

    if event is None:
        pytest.skip("No offline events available for event_offline_get")


@pytest.mark.oauth_only
def test_event_offline_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.event.offline.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    events = bitrix_response.result

    if not events:
        pytest.skip("No offline events available for event_offline_list")

    for event in events:
        assert isinstance(event, dict), "Event should be a dict"

        for field in _FIELDS:
            assert field in event, f"Field '{field}' should be present"


@pytest.mark.oauth_only
def test_event_offline_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.event.offline.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    events = bitrix_response.result

    if not events:
        pytest.skip("No offline events available for event_offline_list.as_list")

    for event in events:
        assert isinstance(event, dict), "Event should be a dict"

        for field in _FIELDS:
            assert field in event, f"Field '{field}' should be present"


@pytest.mark.oauth_only
def test_event_offline_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.event.offline.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    events = bitrix_response.result

    last_event_id = None

    for event in events:
        assert isinstance(event, dict)
        assert "ID" in event

        event_id = int(event["ID"])

        if last_event_id is None:
            last_event_id = event_id
        else:
            assert last_event_id > event_id
            last_event_id = event_id


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_offline_clear")
def test_event_offline_clear(bitrix_client: BaseClient):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    process_id: Text = f"{SDK_NAME}_process_id_{timestamp}"

    bitrix_response = bitrix_client.event.offline.clear(
        process_id=process_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_cleared = bitrix_response.result

    assert is_cleared is True, "Method clear should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_offline_error")
def test_event_offline_error(bitrix_client: BaseClient):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    process_id: Text = f"{SDK_NAME}_process_id_{timestamp}"

    bitrix_response = bitrix_client.event.offline.error(
        process_id=process_id,
        message_id=[_ERROR_MESSAGE_ID],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_success = bitrix_response.result

    assert is_success is True, "Method error should return True"
