from typing import Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse

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
"isAutomationEnabled", "isBizProcEnabled", "isSetOpenPermissions", "createdTime", "updatedTime", "updatedBy")

_TITLE: Text = f"{SDK_NAME} SPA"
_ENTITY_TYPE_ID: int = 1030 + int(Config().get_local_datetime().timestamp() % 1000) * 2
_UPDATED_TITLE: Text = f"{SDK_NAME} Updated SPA"


@pytest.mark.dependency(name="test_type_fields")
def test_type_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.type.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "fields" in result, "Result should contain 'fields' key"

    fields = cast(dict, result["fields"])

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], dict), f"Field {field!r} should be a dictionary"


@pytest.mark.dependency(name="test_type_add", depends=["test_type_fields"])
def test_type_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.type.add(
        fields={
            "title": _TITLE,
            "entityTypeId": _ENTITY_TYPE_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "type" in result, "Result should contain 'type' key"

    type_data = cast(dict, result["type"])
    assert "id" in type_data, "Type should have 'id' field"

    type_id = int(type_data["id"])
    assert type_id > 0, "SPA creation should return a positive ID"

    cache.set("type_id", type_id)


@pytest.mark.dependency(name="test_type_get", depends=["test_type_add"])
def test_type_get(bitrix_client: Client, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    bitrix_response = bitrix_client.crm.type.get(bitrix_id=type_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "type" in result, "Result should contain 'type' key"

    type_data = cast(dict, result["type"])

    assert type_data.get("id") == type_id, "SPA ID does not match"
    assert type_data.get("title") == _TITLE, "SPA title does not match"
    assert int(type_data.get("entityTypeId", 0)) == _ENTITY_TYPE_ID, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_get_by_entity_type_id", depends=["test_type_get"])
def test_type_get_by_entity_type_id(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.type.get_by_entity_type_id(
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "type" in result, "Result should contain 'type' key"

    type_data = cast(dict, result["type"])

    assert int(type_data.get("entityTypeId", 0)) == _ENTITY_TYPE_ID, "SPA entityTypeId does not match"


@pytest.mark.dependency(name="test_type_update", depends=["test_type_get_by_entity_type_id"])
def test_type_update(bitrix_client: Client, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    bitrix_response = bitrix_client.crm.type.update(
        bitrix_id=type_id,
        fields={
            "title": _UPDATED_TITLE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "type" in result, "Result should contain 'type' key"


@pytest.mark.dependency(name="test_type_list", depends=["test_type_update"])
def test_type_list(bitrix_client: Client, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    bitrix_response = bitrix_client.crm.type.list(
        filter={"id": type_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "types" in result, "Result should contain 'types' key"

    types = cast(list, result["types"])

    assert len(types) == 1, "Expected one SPA to be returned"
    type_data = types[0]

    assert isinstance(type_data, dict)
    assert type_data.get("id") == type_id, "SPA ID does not match in list"
    assert type_data.get("title") == _UPDATED_TITLE, "SPA title does not match after update"


@pytest.mark.dependency(name="test_type_list_as_list", depends=["test_type_list"])
def test_type_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.type.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    types = cast(list, bitrix_response.result)

    assert len(types) >= 1, "Expected at least one SPA to be returned"

    for type_data in types:
        assert isinstance(type_data, dict)


@pytest.mark.dependency(name="test_type_delete", depends=["test_type_list_as_list"])
def test_type_delete(bitrix_client: Client, cache: Cache):
    """"""

    type_id = cache.get("type_id", None)
    assert isinstance(type_id, int), "SPA ID should be cached"

    bitrix_response = bitrix_client.crm.type.delete(bitrix_id=type_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)
