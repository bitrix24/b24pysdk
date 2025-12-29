from typing import Iterable, Text, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import (
    BitrixAPIListResponse,
    BitrixAPIResponse,
)

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_category,
]

_ENTITY_TYPE_ID: int = 2
_NAME: Text = f"{SDK_NAME} Test Funnel"
_SORT: int = 500
_IS_DEFAULT: Text = "N"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Funnel"
_UPDATED_SORT: int = 600
_FIELDS_FIELDS: Iterable[Text] = ("id", "name", "sort", "entityTypeId", "isDefault", "originId", "originatorId")


def test_crm_category_fields(bitrix_client: Client):
    """Test retrieving funnel fields."""

    bitrix_response = bitrix_client.crm.category.fields(
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "fields" in result, "Result should contain 'fields' key"

    fields = cast(dict, result["fields"])

    for field in _FIELDS_FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_category_add")
def test_crm_category_add(bitrix_client: Client, cache: Cache):
    """Test creating a new funnel."""

    bitrix_response = bitrix_client.crm.category.add(
        entity_type_id=_ENTITY_TYPE_ID,
        fields={
            "name": _NAME,
            "sort": _SORT,
            "isDefault": _IS_DEFAULT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "category" in result, "Result should contain 'category' key"

    category = cast(dict, result["category"])

    assert isinstance(category, dict)
    assert "id" in category, "Category should have 'id' field"

    category_id = cast(int, category["id"])
    assert category_id > 0, "Funnel creation should return a positive ID"
    assert category.get("name") == _NAME, "Funnel name does not match"
    assert category.get("sort") == _SORT, "Funnel sort does not match"
    assert category.get("isDefault") == _IS_DEFAULT, "Funnel isDefault does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Funnel entityTypeId does not match"

    cache.set("category_id", category_id)


@pytest.mark.dependency(name="test_crm_category_get", depends=["test_crm_category_add"])
def test_crm_category_get(bitrix_client: Client, cache: Cache):
    """Test retrieving a funnel by ID."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached after addition"

    bitrix_response = bitrix_client.crm.category.get(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "category" in result, "Result should contain 'category' key"

    category = cast(dict, result["category"])

    assert isinstance(category, dict)
    assert category.get("id") == category_id, f"Funnel ID does not match. Expected: {category_id}, Got: {category.get('id')}"
    assert category.get("name") == _NAME, "Funnel name does not match"
    assert category.get("sort") == _SORT, "Funnel sort does not match"
    assert category.get("isDefault") == _IS_DEFAULT, "Funnel isDefault does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Funnel entityTypeId does not match"


@pytest.mark.dependency(name="test_crm_category_list", depends=["test_crm_category_get"])
def test_crm_category_list(bitrix_client: Client, cache: Cache):
    """Test retrieving a list of funnels."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "categories" in result, "Result should contain 'categories' key"

    categories = cast(list, result["categories"])

    assert isinstance(categories, list)
    assert len(categories) >= 1, "Expected at least one funnel to be returned"

    for category in categories:
        if all((
            category.get("id") == category_id,
            category.get("name") == _NAME,
            category.get("sort") == _SORT,
            category.get("isDefault") == _IS_DEFAULT,
            category.get("entityTypeId") == _ENTITY_TYPE_ID,
        )):
            break
    else:
        pytest.fail(f"Test funnel with ID {category_id} should be found in list")


@pytest.mark.dependency(name="test_crm_category_list_as_list", depends=["test_crm_category_list"])
def test_crm_category_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.category.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    categories = cast(list, bitrix_response.result)

    assert len(categories) >= 1, "Expected at least one funnel to be returned"

    for category in categories:
        assert isinstance(category, dict)


@pytest.mark.dependency(name="test_crm_category_update", depends=["test_crm_category_list_as_list"])
def test_crm_category_update(bitrix_client: Client, cache: Cache):
    """Test updating an existing funnel."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.update(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
        fields={
            "name": _UPDATED_NAME,
            "sort": _UPDATED_SORT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "category" in result, "Result should contain 'category' key"

    category = cast(dict, result["category"])

    assert isinstance(category, dict)
    assert category.get("id") == category_id, f"Funnel ID does not match. Expected: {category_id}, Got: {category.get('id')}"
    assert category.get("name") == _UPDATED_NAME, "Funnel updated name does not match"
    assert category.get("sort") == _UPDATED_SORT, "Funnel updated sort does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Funnel entityTypeId does not match"


@pytest.mark.dependency(name="test_crm_category_delete", depends=["test_crm_category_update"])
def test_crm_category_delete(bitrix_client: Client, cache: Cache):
    """Test deleting a funnel."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.delete(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    assert result is None, "Funnel deletion should return null"
