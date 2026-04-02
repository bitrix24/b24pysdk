from typing import Generator, Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.entity,
    pytest.mark.entity_item,
]

_NAME: Text = f"{SDK_NAME} Test Item"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Test Item"
_ACTIVE: bool = True
_SORT: int = 500
_PROPERTY_VALUES: dict = {}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_add")
def test_entity_item_add(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.add method."""

    entity_name: Text = f"EI{str(int(Config().get_local_datetime().timestamp() * (10 ** 6)))[:14]}"

    entity_response = bitrix_client.entity.add(
        entity=entity_name,
        name=f"{SDK_NAME} Item Entity",
    ).response
    assert isinstance(entity_response, BitrixAPIResponse)
    assert isinstance(entity_response.result, int)
    assert entity_response.result > 0, "Entity creation should return a positive ID"

    bitrix_response = bitrix_client.entity.item.add(
        entity=entity_name,
        name=_NAME,
        active=_ACTIVE,
        sort=_SORT,
        date_active_from=Config().get_local_date().isoformat(),
        property_values=_PROPERTY_VALUES,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    item_id = bitrix_response.result
    assert item_id > 0, "Item creation should return a positive ID"

    cache.set("entity_item_id", item_id)
    cache.set("entity_item_entity_name", entity_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_get", depends=["test_entity_item_add"])
def test_entity_item_get(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.get method."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    item_id = cache.get("entity_item_id", None)
    assert isinstance(item_id, int), "Item ID should be cached"

    bitrix_response = bitrix_client.entity.item.get(
        entity=entity_name,
        filter={"ID": item_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result
    assert len(items) == 1, "Expected one item to be returned"

    item = items[0]
    assert isinstance(item, dict)
    assert item.get("ID") == str(item_id), "Item ID does not match"
    assert item.get("NAME") == _NAME, "Item NAME does not match"
    assert item.get("ENTITY") == entity_name, "Item ENTITY does not match"
    assert item.get("ACTIVE") == ("Y" if _ACTIVE else "N"), "Item ACTIVE does not match"
    assert item.get("SORT") == str(_SORT), "Item SORT does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_get_as_list", depends=["test_entity_item_get"])
def test_entity_item_get_as_list(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.get().as_list method."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    bitrix_response = bitrix_client.entity.item.get(entity=entity_name).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result
    assert len(items) >= 1, "Expected at least one item to be returned"

    for item in items:
        assert isinstance(item, dict)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_get_as_list_fast", depends=["test_entity_item_get_as_list"])
def test_entity_item_get_as_list_fast(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.get().as_list_fast method."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    bitrix_response = bitrix_client.entity.item.get(
        entity=entity_name,
        sort={"ID": "DESC"},
    ).as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    items = bitrix_response.result
    last_item_id = None

    for item in items:
        assert isinstance(item, dict)
        assert "ID" in item

        item_id = int(item["ID"])
        if last_item_id is None:
            last_item_id = item_id
        else:
            assert last_item_id > item_id
            last_item_id = item_id


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_update", depends=["test_entity_item_get_as_list_fast"])
def test_entity_item_update(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.update method."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    item_id = cache.get("entity_item_id", None)
    assert isinstance(item_id, int), "Item ID should be cached"

    bitrix_response = bitrix_client.entity.item.update(
        entity=entity_name,
        bitrix_id=item_id,
        property_values=_PROPERTY_VALUES,
        name=_UPDATED_NAME,
        active=False,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result
    assert is_updated is True, "Item update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_verify_update", depends=["test_entity_item_update"])
def test_entity_item_verify_update(bitrix_client: BaseClient, cache: Cache):
    """Verify entity.item.update changes."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    item_id = cache.get("entity_item_id", None)
    assert isinstance(item_id, int), "Item ID should be cached"

    bitrix_response = bitrix_client.entity.item.get(
        entity=entity_name,
        filter={"ID": item_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result
    assert len(items) == 1, "Expected one item to be returned"

    item = items[0]
    assert isinstance(item, dict)
    assert item.get("ID") == str(item_id), "Item ID does not match"
    assert item.get("NAME") == _UPDATED_NAME, "Item NAME does not match after update"
    assert item.get("ACTIVE") == "N", "Item ACTIVE does not match after update"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_delete", depends=["test_entity_item_verify_update"])
def test_entity_item_delete(bitrix_client: BaseClient, cache: Cache):
    """Test entity.item.delete method."""

    entity_name = cache.get("entity_item_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    item_id = cache.get("entity_item_id", None)
    assert isinstance(item_id, int), "Item ID should be cached"

    bitrix_response = bitrix_client.entity.item.delete(
        entity=entity_name,
        bitrix_id=item_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Item deletion should return True"

    delete_entity_response = bitrix_client.entity.delete(entity=entity_name).response
    assert isinstance(delete_entity_response, BitrixAPIResponse)
    assert delete_entity_response.result is True, "Entity deletion should return True"
