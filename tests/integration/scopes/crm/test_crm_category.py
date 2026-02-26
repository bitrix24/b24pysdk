from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit
from b24pysdk.constants.crm import EntityTypeID

from ....constants import SDK_NAME, SORT

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_category,
]

_FIELDS_FIELDS: Tuple[Text, ...] = ("id", "name", "sort", "entityTypeId", "isDefault", "originId", "originatorId")
_ENTITY_TYPE_ID: EntityTypeID = EntityTypeID.DEAL
_NAME: Text = f"{SDK_NAME} Category"
_SORT: int = SORT
_IS_DEFAULT: B24BoolLit = B24BoolLit.FALSE
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Category"


@pytest.mark.dependency(name="test_crm_category_fields")
def test_crm_category_fields(bitrix_client: BaseClient):
    """Test retrieving Category fields."""

    bitrix_response = bitrix_client.crm.category.fields(
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "fields" in result, "Result should contain 'fields' key"

    fields = result["fields"]

    for field in _FIELDS_FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field {field!r} should be a dictionary"


@pytest.mark.dependency(name="test_crm_category_add")
def test_crm_category_add(bitrix_client: BaseClient, cache: Cache):
    """Test creating a new Category."""

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

    result = bitrix_response.result

    assert "category" in result, "Result should contain 'category' key"

    category = result["category"]

    assert isinstance(category, dict)
    assert "id" in category, "Category should have 'id' field"
    assert isinstance(category["id"], int)

    category_id = category["id"]

    assert category_id > 0, "Category creation should return a positive ID"
    assert category.get("name") == _NAME, "Category name does not match"
    assert category.get("sort") == _SORT, "Category sort does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Category entityTypeId does not match"
    assert category.get("isDefault") == _IS_DEFAULT, "Category isDefault does not match"

    cache.set("category_id", category_id)


@pytest.mark.dependency(name="test_crm_category_get", depends=["test_crm_category_add"])
def test_crm_category_get(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a Category by ID."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached after addition"

    bitrix_response = bitrix_client.crm.category.get(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "category" in result, "Result should contain 'category' key"

    category = result["category"]

    assert isinstance(category, dict)

    assert category.get("id") == category_id, f"Category ID does not match. Expected: {category_id}, Got: {category.get('id')}"
    assert category.get("name") == _NAME, "Category name does not match"
    assert category.get("sort") == _SORT, "Category sort does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Category entityTypeId does not match"
    assert category.get("isDefault") == _IS_DEFAULT, "Category isDefault does not match"


@pytest.mark.dependency(name="test_crm_category_update", depends=["test_crm_category_get"])
def test_crm_category_update(bitrix_client: BaseClient, cache: Cache):
    """Test updating an existing Category."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.update(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
        fields={
            "name": _UPDATED_NAME,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "category" in result, "Result should contain 'category' key"

    category = result["category"]

    assert isinstance(category, dict)

    assert category.get("id") == category_id, f"Category ID does not match. Expected: {category_id}, Got: {category.get('id')}"
    assert category.get("name") == _UPDATED_NAME, "Category updated name does not match"
    assert category.get("sort") == _SORT, "Category sort does not match"
    assert category.get("entityTypeId") == _ENTITY_TYPE_ID, "Category entityTypeId does not match"
    assert category.get("isDefault") == _IS_DEFAULT, "Category isDefault does not match"


@pytest.mark.dependency(name="test_crm_category_list", depends=["test_crm_category_update"])
def test_crm_category_list(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a list of funnels."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "categories" in result, "Result should contain 'categories' key"

    categories = result["categories"]

    assert isinstance(categories, list)
    assert len(categories) >= 1, "Expected at least one Category to be returned"

    for category in categories:
        if all((
            category.get("id") == category_id,
            category.get("name") == _UPDATED_NAME,
            category.get("sort") == _SORT,
            category.get("entityTypeId") == _ENTITY_TYPE_ID,
            category.get("isDefault") == _IS_DEFAULT,
        )):
            break
    else:
        pytest.fail(f"Test Category with ID {category_id} should be found in list")


@pytest.mark.dependency(name="test_crm_category_list_as_list", depends=["test_crm_category_update"])
def test_crm_category_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.category.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    categories = bitrix_response.result

    assert len(categories) >= 1, "Expected at least one Category to be returned"

    for category in categories:
        assert isinstance(category, dict)


@pytest.mark.dependency(name="test_crm_category_delete", depends=["test_crm_category_add"])
def test_crm_category_delete(bitrix_client: BaseClient, cache: Cache):
    """Test deleting a Category."""

    category_id = cache.get("category_id", None)
    assert isinstance(category_id, int), "Category ID should be cached"

    bitrix_response = bitrix_client.crm.category.delete(
        bitrix_id=category_id,
        entity_type_id=_ENTITY_TYPE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result

    assert result is None, "Category deletion should return None"
