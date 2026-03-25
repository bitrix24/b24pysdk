from datetime import timedelta
from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_resource_booking,
]

_BOOKING_FIELDS: Tuple[Text, ...] = ("ID", "SECTION_ID", "DATE_FROM", "DATE_TO")


@pytest.mark.dependency(name="test_calendar_resource_booking_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    bitrix_response = bitrix_client.calendar.resource.add(
        name=f"{SDK_NAME} BOOKING RESOURCE {int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.resource.add result should be int"

    resource_id = bitrix_response.result
    assert resource_id > 0, "calendar.resource.add should return positive ID"

    cache.set("calendar_resource_booking_id", resource_id)


@pytest.mark.dependency(name="test_calendar_resource_booking_list", depends=["test_calendar_resource_booking_prepare"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_id = cache.get("calendar_resource_booking_id", None)
    assert isinstance(resource_id, int), "Resource ID should be cached"

    from_date = Config().get_local_date().isoformat()
    to_date = (Config().get_local_date() + timedelta(days=30)).isoformat()

    bitrix_response = bitrix_client.calendar.resource.booking.list(
        filter={
            "resourceTypeIdList": [resource_id],
            "from": from_date,
            "to": to_date,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "calendar.resource.booking.list result should be a list"

    bookings = bitrix_response.result
    for booking in bookings:
        assert isinstance(booking, dict), "Each booking should be a dict"
        for field in _BOOKING_FIELDS:
            assert field in booking, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_calendar_resource_booking_cleanup", depends=["test_calendar_resource_booking_list"])
def test_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_id = cache.get("calendar_resource_booking_id", None)
    assert isinstance(resource_id, int), "Resource ID should be cached"

    bitrix_response = bitrix_client.calendar.resource.delete(resource_id=resource_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.resource.delete result should be bool"
    assert bitrix_response.result is True, "calendar.resource.delete should return True"
