from typing import Generator, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_type,
]

_FIELDS: Tuple[Text, ...] = (
    "id", "title", "code", "createdBy", "entityTypeId", "customSectionId", "isCategoriesEnabled", "isStagesEnabled",
    "isBeginCloseDatesEnabled", "isClientEnabled", "isUseInUserfieldEnabled", "isLinkWithProductsEnabled",
    "isMycompanyEnabled", "isDocumentsEnabled", "isSourceEnabled", "isObserversEnabled", "isRecyclebinEnabled",
    "isAutomationEnabled", "isBizProcEnabled", "isSetOpenPermissions", "createdTime", "updatedTime", "updatedBy",
)

_TITLE: Text = f"{SDK_NAME} SPA"
_UPDATED_TITLE: Text = f"{SDK_NAME} Updated SPA"


@pytest.mark.dependency(name="test_type_fields")
def test_type_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.type.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "fields" in result, "Result should contain 'fields' key"

    fields = result["fields"]

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], dict), f"Field {field!r} should be a dictionary"


@pytest.mark.dependency(name="test_type_add")
def test_type_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.type.add(
        fields={
            "title": _TITLE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "type" in result, "Result should contain 'type' key"

    type_data = result["type"]

    assert "id" in type_data, "Type should have 'id' field"
    assert isinstance(type_data["id"], int)

    assert "entityTypeId" in type_data, "Type should have 'entityTypeId' field"
    assert isinstance(type_data["entityTypeId"], int)

    type_id = type_data["id"]
    assert type_id > 0, "SPA creation should return a positive ID"

    entity_type_id = type_data["entityTypeId"]
    assert entity_type_id > 0, "SPA creation should return a positive entity type ID"

    cache.set("type_id", type_id)
    cache.set("entity_type_id", entity_type_id)


@pytest.mark.dependency(name="test_type_get", depends=["test_type_add"])
def test_type_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    entity_type_id = cache.get("entity_type_id", None)
    assert isinstance(entity_type_id, int), "SPA entity type ID should be cached"

    bitrix_response = bitrix_client.crm.type.get(bitrix_id=type_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "type" in result, "Result should contain 'type' key"

    type_data = result["type"]

    assert type_data.get("id") == type_id, "SPA ID does not match"
    assert type_data.get("title") == _TITLE, "SPA title does not match"
    assert type_data.get("entityTypeId") == entity_type_id, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_get_by_entity_type_id", depends=["test_type_get"])
def test_type_get_by_entity_type_id(bitrix_client: BaseClient, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    entity_type_id = cache.get("entity_type_id", None)
    assert isinstance(entity_type_id, int), "SPA entity type ID should be cached"

    bitrix_response = bitrix_client.crm.type.get_by_entity_type_id(
        entity_type_id=entity_type_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "type" in result, "Result should contain 'type' key"

    type_data = result["type"]

    assert type_data.get("id") == type_id, "SPA ID does not match"
    assert type_data.get("title") == _TITLE, "SPA title does not match"
    assert type_data.get("entityTypeId") == entity_type_id, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_update", depends=["test_type_get_by_entity_type_id"])
def test_type_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    entity_type_id = cache.get("entity_type_id", None)
    assert isinstance(entity_type_id, int), "SPA entity type ID should be cached"

    bitrix_response = bitrix_client.crm.type.update(
        bitrix_id=type_id,
        fields={
            "title": _UPDATED_TITLE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "type" in result, "Result should contain 'type' key"

    type_data = result["type"]

    assert type_data.get("id") == type_id, "SPA ID does not match"
    assert type_data.get("title") == _UPDATED_TITLE, "SPA title does not match"
    assert type_data.get("entityTypeId") == entity_type_id, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_list", depends=["test_type_update"])
def test_type_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    entity_type_id = cache.get("entity_type_id", None)
    assert isinstance(entity_type_id, int), "SPA entity type ID should be cached"

    bitrix_response = bitrix_client.crm.type.list(
        filter={
            "id": type_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "types" in result, "Result should contain 'types' key"

    types = result["types"]

    assert len(types) == 1, "Expected one SPA to be returned"
    type_data = types[0]

    assert isinstance(type_data, dict)

    assert type_data.get("id") == type_id, "SPA ID does not match in list"
    assert type_data.get("title") == _UPDATED_TITLE, "SPA title does not match after update"
    assert type_data.get("entityTypeId") == entity_type_id, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_list_as_list", depends=["test_type_update"])
def test_type_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.type.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    types = bitrix_response.result

    assert len(types) >= 1, "Expected at least one SPA to be returned"

    for type_data in types:
        assert isinstance(type_data, dict)


@pytest.mark.dependency(name="test_type_list_as_list_fast", depends=["test_type_update"])
def test_type_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.type.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    types = bitrix_response.result

    last_type_id = None

    for type_data in types:
        assert isinstance(type_data, dict)
        assert "id" in type_data

        type_id = type_data["id"]

        if last_type_id is None:
            last_type_id = type_id
        else:
            assert last_type_id > type_id
            last_type_id = type_id


@pytest.mark.dependency(name="test_type_delete", depends=["test_type_add"])
def test_type_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    bitrix_response = bitrix_client.crm.type.delete(bitrix_id=type_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    result = bitrix_response.result

    assert result == [], "Digital workplace deletion should return []"
