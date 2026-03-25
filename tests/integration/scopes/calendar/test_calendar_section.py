from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_section,
]

_SECTION_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "CAL_TYPE", "OWNER_ID")
_UPDATED_NAME: Text = f"{SDK_NAME} SECTION UPDATED"


@pytest.mark.dependency(name="test_calendar_section_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_name = f"{SDK_NAME} SECTION {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.calendar.section.add(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        name=section_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.section.add result should be int"

    section_id = bitrix_response.result
    assert section_id > 0, "calendar.section.add should return positive ID"

    cache.set("calendar_section_id", section_id)
    cache.set("calendar_section_name", section_name)


@pytest.mark.dependency(name="test_calendar_section_update", depends=["test_calendar_section_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_id = cache.get("calendar_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.section.update(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        bitrix_id=str(section_id),
        name=_UPDATED_NAME,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.section.update result should be int"
    assert bitrix_response.result > 0, "calendar.section.update should return positive ID"


@pytest.mark.dependency(name="test_calendar_section_get", depends=["test_calendar_section_update"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_id = cache.get("calendar_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.section.get(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "calendar.section.get result should be a list"

    sections = bitrix_response.result
    assert len(sections) >= 1, "Expected at least one section to be returned"

    target_section = None
    for section in sections:
        assert isinstance(section, dict), "Each section should be a dict"
        for field in _SECTION_FIELDS:
            assert field in section, f"Field '{field}' should be present"

        if section.get("ID") == str(section_id):
            target_section = section

    assert target_section is not None, "Created section should be present in calendar.section.get result"
    assert target_section.get("NAME") == _UPDATED_NAME, "Section NAME does not match"
    assert target_section.get("CAL_TYPE") == "user", "Section CAL_TYPE does not match"
    assert target_section.get("OWNER_ID") == str(BITRIX_PORTAL_OWNER_ID), "Section OWNER_ID does not match"


@pytest.mark.dependency(name="test_calendar_section_delete", depends=["test_calendar_section_get"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    section_id = cache.get("calendar_section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.calendar.section.delete(
        type="user",
        owner_id=BITRIX_PORTAL_OWNER_ID,
        bitrix_id=section_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.section.delete result should be bool"
    assert bitrix_response.result is True, "calendar.section.delete should return True"
