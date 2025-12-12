from typing import Dict, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.entity,
]

_FIELDS: Tuple[Text, ...] = ("ENTITY", "NAME")
_ACCESS: Dict = {"AU": "R"}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_add")
def test_entity_add(bitrix_client: Client, cache: Cache):
    """"""

    entity_name: Text = f"ENTITY_{str(Config().get_local_datetime().timestamp() * (10 ** 6))[:8]}"

    bitrix_response = bitrix_client.entity.add(
        entity=entity_name,
        name=f"{SDK_NAME} Test Entity",
        access=_ACCESS,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    entity_id = cast(int, bitrix_response.result)
    assert entity_id > 0, "Entity creation should return a positive ID"

    cache.set("entity_name", entity_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_get", depends=["test_entity_add"])
def test_entity_get(bitrix_client: Client, cache: Cache):
    """"""

    entity_name = cache.get("entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached after addition"

    bitrix_response = bitrix_client.entity.get(
        entity=entity_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    entity = cast(dict, bitrix_response.result)

    assert entity.get("ENTITY") == entity_name, "Entity ENTITY does not match"
    assert entity.get("NAME") == f"{SDK_NAME} Test Entity", "Entity NAME does not match"


@pytest.mark.oauth_only
def test_entity_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.entity.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    entities = cast(list, bitrix_response.result)

    assert len(entities) >= 1, "Expected at least one entities to be returned"

    for entity in entities:
        assert isinstance(entity, dict)
        for field in _FIELDS:
            assert field in entity, f"Field '{field}' should be present"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_update", depends=["test_entity_add"])
def test_entity_update(bitrix_client: Client, cache: Cache):
    """"""

    entity_name = cache.get("entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    bitrix_response = bitrix_client.entity.update(
        entity=entity_name,
        name=f"{SDK_NAME} Updated Test Entity",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Entity update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_rights", depends=["test_entity_add"])
def test_entity_rights(bitrix_client: Client, cache: Cache):
    """"""

    entity_name = cache.get("entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    bitrix_response = bitrix_client.entity.rights(
        entity=entity_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    rights = cast(dict, bitrix_response.result)
    assert isinstance(rights, dict), "Rights should be a dictionary"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_delete", depends=["test_entity_add"])
def test_entity_delete(bitrix_client: Client, cache: Cache):
    """"""

    entity_name = cache.get("entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    bitrix_response = bitrix_client.entity.delete(
        entity=entity_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Entity deletion should return True"
