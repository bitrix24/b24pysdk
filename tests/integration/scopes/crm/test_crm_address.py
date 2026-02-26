from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants.crm import AddressType, EntityTypeID

from ....constants import LEAD_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_address,
]

_FIELDS: Tuple[Text, ...] = ("TYPE_ID", "ENTITY_TYPE_ID", "ENTITY_ID", "ADDRESS_1", "ADDRESS_2", "CITY", "POSTAL_CODE", "REGION", "PROVINCE", "COUNTRY", "LOC_ADDR_ID", "ANCHOR_TYPE_ID", "ANCHOR_ID")
_TYPE_ID: AddressType = AddressType.ACTUAL
_ENTITY_TYPE_ID: EntityTypeID = EntityTypeID.LEAD
_ENTITY_ID: int = LEAD_ID
_ADDRESS_1: Text = f"{SDK_NAME} Address, 1"
_ADDRESS_2: Text = f"{SDK_NAME} Address, 2"
_CITY: Text = f"{SDK_NAME} City"
_POSTAL_CODE: Text = "123456"
_REGION: Text = f"{SDK_NAME} Region"
_PROVINCE: Text = f"{SDK_NAME} Province"
_COUNTRY: Text = f"{SDK_NAME} Country"


@pytest.mark.dependency(name="test_crm_address_fields")
def test_crm_address_fields(bitrix_client: BaseClient):
    """Test retrieving address fields."""

    bitrix_response = bitrix_client.crm.address.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_address_add")
def test_crm_address_add(bitrix_client: BaseClient):
    """Test adding a new address."""

    bitrix_response = bitrix_client.crm.address.add(
        fields={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": _ENTITY_ID,
            "ADDRESS_1": _ADDRESS_1,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_added = bitrix_response.result

    assert is_added is True, "Address addition should return True"


@pytest.mark.dependency(name="test_crm_address_update", depends=["test_crm_address_add"])
def test_crm_address_update(bitrix_client: BaseClient):
    """Test updating an address."""

    bitrix_response = bitrix_client.crm.address.update(
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

    is_updated = bitrix_response.result

    assert is_updated is True, "Address update should return True"


@pytest.mark.dependency(name="test_crm_address_list", depends=["test_crm_address_update"])
def test_crm_address_list(bitrix_client: BaseClient):
    """Test retrieving a list of addresses."""

    bitrix_response = bitrix_client.crm.address.list(
        select=list(_FIELDS),
        filter={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": _ENTITY_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    addresses = bitrix_response.result

    assert len(addresses) == 1, "Expected one address to be returned"

    address = addresses[0]

    assert isinstance(address, dict)

    assert address.get("TYPE_ID") == str(_TYPE_ID), "TYPE_ID does not match"
    assert address.get("ENTITY_TYPE_ID") == str(_ENTITY_TYPE_ID), "ENTITY_TYPE_ID does not match"
    assert address.get("ENTITY_ID") == str(_ENTITY_ID), "ENTITY_ID does not match"
    assert address.get("ADDRESS_1") == _ADDRESS_1, "ADDRESS_1 does not match"
    assert address.get("ADDRESS_2") == _ADDRESS_2, "ADDRESS_2 does not match"
    assert address.get("CITY") == _CITY, "CITY does not match"
    assert address.get("POSTAL_CODE") == _POSTAL_CODE, "POSTAL_CODE does not match"
    assert address.get("REGION") == _REGION, "REGION does not match"
    assert address.get("PROVINCE") == _PROVINCE, "PROVINCE does not match"
    assert address.get("COUNTRY") == _COUNTRY, "COUNTRY does not match"


@pytest.mark.dependency(name="test_crm_address_list_as_list", depends=["test_crm_address_update"])
def test_crm_address_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.address.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    addresses = bitrix_response.result

    assert len(addresses) >= 1, "Expected at least one address to be returned"

    for address in addresses:
        assert isinstance(address, dict)


@pytest.mark.dependency(name="test_crm_address_delete", depends=["test_crm_address_add"])
def test_crm_address_delete(bitrix_client: BaseClient):
    """Test deleting an address."""

    bitrix_response = bitrix_client.crm.address.delete(
        fields={
            "TYPE_ID": _TYPE_ID,
            "ENTITY_TYPE_ID": _ENTITY_TYPE_ID,
            "ENTITY_ID": _ENTITY_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result

    assert is_deleted is True, "Address deletion should return True"
