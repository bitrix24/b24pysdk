from typing import Generator, Text, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.entity,
    pytest.mark.entity_section,
]

_ENTITY: Text = "test_entity"
_NAME: Text = f"{SDK_NAME} Test Section"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Test Section"
_SORT: int = 100
_ACTIVE: bool = True
_DESCRIPTION: Text = f"{SDK_NAME} Test Section Description"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_add")
def test_section_add(bitrix_client: Client, cache: Cache):
    """"""

    unique_name = f"{_NAME}_{int(Config().get_local_datetime().timestamp())}"

    bitrix_response = bitrix_client.entity.section.add(
        entity=_ENTITY,
        name=unique_name,
        sort=_SORT,
        active=_ACTIVE,
        description=_DESCRIPTION,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    section_id = cast(int, bitrix_response.result)

    assert section_id > 0, "Section creation should return a positive ID"

    cache.set("section_id", section_id)
    cache.set("section_name", unique_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_get", depends=["test_section_add"])
def test_section_get(bitrix_client: Client, cache: Cache):
    """"""

    section_id = cache.get("section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    section_name = cache.get("section_name", None)
    assert isinstance(section_name, str), "Section name should be cached"

    bitrix_response = bitrix_client.entity.section.get(
        entity=_ENTITY,
        filter={"ID": section_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    sections = cast(list, bitrix_response.result)

    assert len(sections) == 1, "Expected one section to be returned"
    section = sections[0]

    assert isinstance(section, dict)
    assert section.get("ID") == str(section_id), "Returned section ID does not match expected"
    assert section.get("NAME") == section_name, "Section NAME does not match"
    assert section.get("ENTITY") == _ENTITY, "Section ENTITY does not match"
    assert section.get("ACTIVE") == ("Y" if _ACTIVE else "N"), "Section ACTIVE does not match"
    assert section.get("SORT") == str(_SORT), "Section SORT does not match"
    assert section.get("DESCRIPTION") == _DESCRIPTION, "Section DESCRIPTION does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_get_as_list", depends=["test_section_add"])
def test_section_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.entity.section.get(
        entity=_ENTITY,
    ).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    sections = cast(list, bitrix_response.result)
    assert len(sections) >= 1, "Expected at least one section to be returned"

    for section in sections:
        assert isinstance(section, dict)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_get_as_list_fast", depends=["test_section_add"])
def test_section_get_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.entity.section.get(
        entity=_ENTITY,
        sort={"ID": "DESC"},
    ).as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    sections = cast(Generator, bitrix_response.result)

    last_section_id = None

    for section in sections:
        assert isinstance(section, dict)
        assert "ID" in section

        section_id = int(section["ID"])

        if last_section_id is None:
            last_section_id = section_id
        else:
            assert last_section_id > section_id
            last_section_id = section_id


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_update", depends=["test_section_get"])
def test_section_update(bitrix_client: Client, cache: Cache):
    """"""

    section_id = cache.get("section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.entity.section.update(
        entity=_ENTITY,
        bitrix_id=section_id,
        name=_UPDATED_NAME,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Section update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_section_delete", depends=["test_section_update"])
def test_section_delete(bitrix_client: Client, cache: Cache):
    """"""

    section_id = cache.get("section_id", None)
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.entity.section.delete(
        entity=_ENTITY,
        bitrix_id=section_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Section deletion should return True"
