from datetime import timedelta

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_meeting_status,
]


@pytest.mark.dependency(name="test_calendar_meeting_status_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_response = bitrix_client.calendar.section.add(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        name=f"{SDK_NAME} MEETING STATUS SECTION {int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
    ).response

    assert isinstance(section_response, BitrixAPIResponse)
    assert isinstance(section_response.result, int), "calendar.section.add result should be int"
    assert section_response.result > 0, "calendar.section.add should return positive ID"
    cache.set("calendar_meeting_status_section_id", section_response.result)

    dt_start = Config().get_local_datetime()
    dt_end = dt_start + timedelta(hours=1)

    event_response = bitrix_client.calendar.event.add(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        from_date=dt_start.isoformat(),
        to=dt_end.isoformat(),
        section=section_response.result,
        name=f"{SDK_NAME} MEETING STATUS EVENT",
        attendees=[BITRIX_PORTAL_OWNER_ID],
        host=BITRIX_PORTAL_OWNER_ID,
        is_meeting="Y",
    ).response

    assert isinstance(event_response, BitrixAPIResponse)
    assert isinstance(event_response.result, int), "calendar.event.add result should be int"
    assert event_response.result > 0, "calendar.event.add should return positive ID"
    cache.set("calendar_meeting_status_event_id", event_response.result)


@pytest.mark.dependency(depends=["test_calendar_meeting_status_prepare"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_meeting_status_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    bitrix_response = bitrix_client.calendar.meeting.status.get(event_id=event_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is None or isinstance(
        bitrix_response.result,
        str,
    ), "calendar.meeting.status.get result should be string or None"

    if isinstance(bitrix_response.result, str):
        assert bitrix_response.result in ("Y", "N", "Q"), "calendar.meeting.status.get should return one of: Y, N, Q"


@pytest.mark.dependency(depends=["test_calendar_meeting_status_prepare"])
def test_set(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_meeting_status_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"

    bitrix_response = bitrix_client.calendar.meeting.status.set(event_id=event_id, status="Y").response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.meeting.status.set result should be bool"
    assert bitrix_response.result is True, "calendar.meeting.status.set should return True"


@pytest.mark.dependency(depends=["test_calendar_meeting_status_prepare"])
def test_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    event_id = cache.get("calendar_meeting_status_event_id", None)
    assert isinstance(event_id, int), "Event ID should be cached"
    bitrix_response = bitrix_client.calendar.event.delete(bitrix_id=event_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.event.delete result should be bool"
    assert bitrix_response.result is True, "calendar.event.delete should return True"

    section_id = cache.get("calendar_meeting_status_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"
    bitrix_response = bitrix_client.calendar.section.delete(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        bitrix_id=section_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.section.delete result should be bool"
    assert bitrix_response.result is True, "calendar.section.delete should return True"
