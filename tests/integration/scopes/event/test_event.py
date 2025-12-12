from typing import Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.constants.event import EventType

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.event,
]

_FIELDS: Tuple[Text, ...] = ("event", "handler", "auth_type", "offline")
_EVENT_NAME: Text = "ONCRMLEADADD"
_HANDLER: Text = "https://example.com/handler/"
_EVENT_TYPE: EventType = EventType.ONLINE
_UNBIND_RESULT_FIELD: Text = "count"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_bind")
def test_event_bind(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.event.bind(
        event=_EVENT_NAME,
        handler=_HANDLER,
        auth_type=BITRIX_PORTAL_OWNER_ID,
        event_type=_EVENT_TYPE,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_bound = cast(bool, bitrix_response.result)

    assert is_bound is True, "Event binding should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_get", depends=["test_event_bind"])
def test_event_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.event.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    events = cast(list, bitrix_response.result)

    assert len(events) >= 1, "Expected at least one event to be returned"

    for event in events:
        assert isinstance(event, dict)

        for field in _FIELDS:
            assert field in event, f"Field '{field}' should be present"

        if all((
            event.get("event") == _EVENT_NAME,
            event.get("handler") == _HANDLER,
            event.get("auth_type") == str(BITRIX_PORTAL_OWNER_ID),
        )):
            break
    else:
        pytest.fail(f"Event '{_EVENT_NAME}' with handler '{_HANDLER}' should be found")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_get_as_list", depends=["test_event_bind"])
def test_event_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.event.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    events = cast(list, bitrix_response.result)

    assert len(events) >= 1, "Expected at least one event to be returned"

    for event in events:
        assert isinstance(event, dict), "Event should be a dict"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_event_unbind", depends=["test_event_get_as_list"])
def test_event_unbind(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.event.unbind(
        event=_EVENT_NAME,
        handler=_HANDLER,
        auth_type=BITRIX_PORTAL_OWNER_ID,
        event_type=_EVENT_TYPE,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    unbind_result = cast(dict, bitrix_response.result)

    assert _UNBIND_RESULT_FIELD in unbind_result, f"Field {_UNBIND_RESULT_FIELD!r} should be present"

    unbind_count = unbind_result[_UNBIND_RESULT_FIELD]

    assert isinstance(unbind_count, int), f"Field '{_UNBIND_RESULT_FIELD}' should be an integer"
    assert unbind_count > 0, "Unbind count should be positive"
