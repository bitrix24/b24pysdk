from typing import Iterable, Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import (
    BitrixAPIListResponse,
    BitrixAPIResponse,
)

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_address,
]

_FIELDS: Iterable[Text] = ("TYPE_ID", "ENTITY_TYPE_ID", "ENTITY_ID", "ADDRESS_1", "ADDRESS_2", "CITY", "POSTAL_CODE", "REGION", "PROVINCE", "COUNTRY")
_TYPE_ID: int = 1
_ENTITY_TYPE_ID: int = 8
_ENTITY_ID: int = 10
_ADDRESS_1: Text = f"{SDK_NAME} Street, 1"
_ADDRESS_2: Text = f"{SDK_NAME} Office 101"
_CITY: Text = f"{SDK_NAME} City"
_POSTAL_CODE: Text = "123456"
_REGION: Text = f"{SDK_NAME} Region"
_PROVINCE: Text = f"{SDK_NAME} Province"
_COUNTRY: Text = f"{SDK_NAME} Country"


@pytest.mark.dependency(name="test_crm_address_fields")
def test_crm_address_fields(bitrix_client: Client):
    """Test retrieving address fields."""

    bitrix_response = bitrix_client.crm.address.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_address_add", depends=["test_crm_address_fields"])
def test_crm_address_add(bitrix_client: Client):
    """Test adding a new address."""

    bitrix_response = bitrix_client.crm.address.add(
        fields={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": _ENTITY_ID,
            "ADDRESS_1": _ADDRESS_1,
            "ADDRESS_2": _ADDRESS_2,
            "CITY": _CITY,
            "POSTAL_CODE": _POSTAL_CODE,
            "REGION": _REGION,
            "PROVINCE": _PROVINCE,
            "COUNTRY": _COUNTRY,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_added = cast(bool, bitrix_response.result)

    assert is_added is True, "Address addition should return True"


@pytest.mark.dependency(name="test_crm_address_list", depends=["test_crm_address_add"])
def test_crm_address_list(bitrix_client: Client):
    """Test retrieving a list of addresses."""

    bitrix_response = bitrix_client.crm.address.list(
        select=list(_FIELDS),
        filter={"TYPE_ID": _TYPE_ID, "ENTITY_TYPE_ID": _ENTITY_TYPE_ID},
        order={"TYPE_ID": "asc"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    addresses = cast(list, bitrix_response.result)

    assert len(addresses) >= 1, "Expected at least one address to be returned"

    for address in addresses:
        assert isinstance(address, dict)
        if all((
            address.get("TYPE_ID") == str(_TYPE_ID),
            address.get("ENTITY_TYPE_ID") == str(_ENTITY_TYPE_ID),
            address.get("ADDRESS_1") == _ADDRESS_1,
            address.get("ADDRESS_2") == _ADDRESS_2,
            address.get("CITY") == _CITY,
            address.get("POSTAL_CODE") == _POSTAL_CODE,
            address.get("REGION") == _REGION,
            address.get("PROVINCE") == _PROVINCE,
            address.get("COUNTRY") == _COUNTRY,
        )):
            break
    else:
        pytest.fail("Test address should be found in list")


@pytest.mark.dependency(name="test_crm_address_list_as_list", depends=["test_crm_address_list"])
def test_crm_address_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.address.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    addresses = cast(list, bitrix_response.result)

    assert len(addresses) >= 1, "Expected at least one address to be returned"

    for address in addresses:
        assert isinstance(address, dict)


@pytest.mark.dependency(name="test_crm_address_update", depends=["test_crm_address_list_as_list"])
def test_crm_address_update(bitrix_client: Client):
    """Test updating an address."""

    bitrix_response_list = bitrix_client.crm.address.list(
        filter={"TYPE_ID": _TYPE_ID, "ENTITY_TYPE_ID": _ENTITY_TYPE_ID},
        order={"ENTITY_ID": "asc"},
    ).response

    assert isinstance(bitrix_response_list, BitrixAPIResponse)
    addresses = cast(list, bitrix_response_list.result)

    assert len(addresses) >= 1, "Expected at least one address to be returned"
    existing_address = addresses[0]
    existing_entity_id = int(existing_address["ENTITY_ID"])

    bitrix_response = bitrix_client.crm.address.update(
        fields={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": existing_entity_id,
            "ADDRESS_1": f"{_ADDRESS_1} Updated",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Address update should return True"


@pytest.mark.dependency(name="test_crm_address_delete", depends=["test_crm_address_update"])
def test_crm_address_delete(bitrix_client: Client):
    """Test deleting an address."""

    bitrix_response = bitrix_client.crm.address.delete(
        fields={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": _ENTITY_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Address deletion should return True"
