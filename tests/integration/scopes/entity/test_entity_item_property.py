from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.entity,
    pytest.mark.entity_item_property,
]

_PROPERTY_NAME: Text = f"{SDK_NAME} Property"
_UPDATED_PROPERTY_NAME: Text = f"{SDK_NAME} Updated Property"
_PROPERTY_FIELDS = ("PROPERTY", "NAME", "TYPE")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_property_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    entity_name: Text = f"EP{str(int(Config().get_local_datetime().timestamp() * (10 ** 6)))[:14]}"
    property_code: Text = f"PROPERTY_{str(int(Config().get_local_datetime().timestamp() * (10 ** 6)))[:10]}"

    entity_response = bitrix_client.entity.add(
        entity=entity_name,
        name=f"{SDK_NAME} Property Entity",
    ).response
    assert isinstance(entity_response, BitrixAPIResponse)
    assert isinstance(entity_response.result, int)
    assert entity_response.result > 0, "Entity creation should return a positive ID"

    bitrix_response = bitrix_client.entity.item.property.add(
        entity=entity_name,
        property=property_code,
        name=_PROPERTY_NAME,
        type="S",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "entity.item.property.add should return bool"
    assert bitrix_response.result is True, "entity.item.property.add should return True"

    cache.set("entity_item_property_entity_name", entity_name)
    cache.set("entity_item_property_code", property_code)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_property_get", depends=["test_entity_item_property_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    entity_name = cache.get("entity_item_property_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    property_code = cache.get("entity_item_property_code", None)
    assert isinstance(property_code, str), "Property code should be cached"

    bitrix_response = bitrix_client.entity.item.property.get(
        entity=entity_name,
        property=property_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "entity.item.property.get should return dict"

    property_data = bitrix_response.result
    for field in _PROPERTY_FIELDS:
        assert field in property_data, f"Field '{field}' should be present"
    assert property_data.get("PROPERTY") == property_code, "Property code does not match"
    assert property_data.get("NAME") == _PROPERTY_NAME, "Property name does not match"
    assert property_data.get("TYPE") == "S", "Property type does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_property_update", depends=["test_entity_item_property_get"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    entity_name = cache.get("entity_item_property_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    property_code = cache.get("entity_item_property_code", None)
    assert isinstance(property_code, str), "Property code should be cached"

    bitrix_response = bitrix_client.entity.item.property.update(
        entity=entity_name,
        property=property_code,
        name=_UPDATED_PROPERTY_NAME,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "entity.item.property.update should return bool"
    assert bitrix_response.result is True, "entity.item.property.update should return True"

    verify_response = bitrix_client.entity.item.property.get(
        entity=entity_name,
        property=property_code,
    ).response
    assert isinstance(verify_response, BitrixAPIResponse)
    assert isinstance(verify_response.result, dict), "entity.item.property.get should return dict"

    property_data = verify_response.result
    for field in _PROPERTY_FIELDS:
        assert field in property_data, f"Field '{field}' should be present"
    assert property_data.get("PROPERTY") == property_code, "Property code does not match after update"
    assert property_data.get("NAME") == _UPDATED_PROPERTY_NAME, "Property name does not match after update"
    assert property_data.get("TYPE") == "S", "Property type does not match after update"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_entity_item_property_delete", depends=["test_entity_item_property_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    entity_name = cache.get("entity_item_property_entity_name", None)
    assert isinstance(entity_name, str), "Entity name should be cached"

    property_code = cache.get("entity_item_property_code", None)
    assert isinstance(property_code, str), "Property code should be cached"

    bitrix_response = bitrix_client.entity.item.property.delete(
        entity=entity_name,
        property=property_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "entity.item.property.delete should return bool"
    assert bitrix_response.result is True, "entity.item.property.delete should return True"

    delete_entity_response = bitrix_client.entity.delete(entity=entity_name).response
    assert isinstance(delete_entity_response, BitrixAPIResponse)
    assert delete_entity_response.result is True, "Entity deletion should return True"
