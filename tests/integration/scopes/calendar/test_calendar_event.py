from datetime import timedelta
from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPINotFound

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_event,
]

_EVENT_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SECTION_ID", "OWNER_ID", "DATE_FROM", "DATE_TO")
_UPDATED_NAME: Text = f"{SDK_NAME} EVENT UPDATED"


@pytest.mark.dependency(name="test_calendar_event_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_name = f"{SDK_NAME} EVENT SECTION {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.calendar.section.add(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        name=section_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.section.add result should be int"

    section_id = bitrix_response.result
    assert section_id > 0, "calendar.section.add should return positive ID"
    cache.set("calendar_event_section_id", section_id)


@pytest.mark.dependency(name="test_calendar_event_add", depends=["test_calendar_event_prepare"])
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_id = cache.get("calendar_event_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    dt_start = Config().get_local_datetime() + timedelta(hours=1)
    dt_end = dt_start + timedelta(hours=1)

    bitrix_response = bitrix_client.calendar.event.add(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        from_date=dt_start.isoformat(),
        to=dt_end.isoformat(),
        section=section_id,
        name=f"{SDK_NAME} EVENT",
        attendees=[BITRIX_PORTAL_OWNER_ID],
        host=BITRIX_PORTAL_OWNER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.event.add result should be int"

    event_id = bitrix_response.result
    assert event_id > 0, "calendar.event.add should return positive ID"
    cache.set("calendar_event_id", event_id)


@pytest.mark.dependency(name="test_calendar_event_update", depends=["test_calendar_event_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    bitrix_response = bitrix_client.calendar.event.update(
        bitrix_id=event_id,
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        name=_UPDATED_NAME,
        attendees=[BITRIX_PORTAL_OWNER_ID],
        host=BITRIX_PORTAL_OWNER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.event.update result should be int"
    assert bitrix_response.result > 0, "calendar.event.update should return positive ID"


@pytest.mark.dependency(name="test_calendar_event_get", depends=["test_calendar_event_update"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    section_id = cache.get("calendar_event_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.event.get(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        section=[section_id],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "calendar.event.get result should be a list"

    events = bitrix_response.result
    assert len(events) >= 1, "Expected at least one event to be returned"

    target_event = None
    for event in events:
        assert isinstance(event, dict), "Each event should be a dict"
        for field in _EVENT_FIELDS:
            assert field in event, f"Field '{field}' should be present"

        if event.get("ID") == str(event_id):
            target_event = event

    assert target_event is not None, "Created event should be present in calendar.event.get result"
    assert target_event.get("NAME") == _UPDATED_NAME, "Event NAME does not match"
    assert target_event.get("SECTION_ID") == str(section_id), "Event SECTION_ID does not match"
    assert target_event.get("OWNER_ID") == str(BITRIX_PORTAL_OWNER_ID), "Event OWNER_ID does not match"


@pytest.mark.dependency(name="test_calendar_event_get_by_id", depends=["test_calendar_event_update"])
def test_get_by_id(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    section_id = cache.get("calendar_event_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.event.get_by_id(bitrix_id=event_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "calendar.event.get_by_id result should be a dict"

    event = bitrix_response.result
    for field in _EVENT_FIELDS:
        assert field in event, f"Field '{field}' should be present"

    assert event.get("ID") == str(event_id), "Event ID does not match"
    assert event.get("NAME") == _UPDATED_NAME, "Event NAME does not match"
    assert event.get("SECTION_ID") == str(section_id), "Event SECTION_ID does not match"
    assert event.get("OWNER_ID") == str(BITRIX_PORTAL_OWNER_ID), "Event OWNER_ID does not match"


def test_get_nearest(bitrix_client: BaseClient):
    """"""

    try:
        bitrix_response = bitrix_client.calendar.event.get.nearest(
            type="user",
            owner_id=BITRIX_PORTAL_OWNER_ID,
            days=30,
        ).response
    except BitrixAPINotFound:
        pytest.skip("calendar.event.get.nearest is not available on this portal")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "calendar.event.get.nearest result should be a list"

    for event in bitrix_response.result:
        assert isinstance(event, dict), "Each nearest event should be a dict"
        for field in ("ID", "NAME"):
            assert field in event, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_calendar_event_delete", depends=["test_calendar_event_get_by_id"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    bitrix_response = bitrix_client.calendar.event.delete(bitrix_id=event_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.event.delete result should be bool"
    assert bitrix_response.result is True, "calendar.event.delete should return True"


@pytest.mark.dependency(name="test_calendar_event_cleanup", depends=["test_calendar_event_delete"])
def test_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_id = cache.get("calendar_event_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.section.delete(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        bitrix_id=section_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.section.delete result should be bool"
    assert bitrix_response.result is True, "calendar.section.delete should return True"
