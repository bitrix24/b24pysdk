from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse, BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.enum import CRMEnumItem, OrderOwnerType
from b24pysdk.schemas.crm.field import CRMField, CRMFieldsDict

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_enum,
]

_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SYMBOL_CODE", "SYMBOL_CODE_SHORT")

_COMMON_ENUM_METHODS: Tuple[Text, ...] = (
    "activitydirection",
    "activitynotifytype",
    "activitypriority",
    "activitystatus",
    "activitytype",
    "addresstype",
    "contenttype",
    "ownertype",
)


def test_crm_enum_fields(bitrix_client: BaseClient):
    """Test retrieving CRM enum field descriptions."""

    bitrix_response = bitrix_client.crm.enum.fields().response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    fields = bitrix_response.value

    assert isinstance(fields, CRMFieldsDict), "CRM enum fields value should be CRMFieldsDict"

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], CRMField), f"Field {field!r} should be CRMField"


@pytest.mark.parametrize("method_name", _COMMON_ENUM_METHODS)
def test_crm_enum_common_values(bitrix_client: BaseClient, method_name: Text):
    """Test CRM enum methods that return common CRMEnumItem values."""

    bitrix_response = getattr(bitrix_client.crm.enum, method_name)().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)

    enum_items = bitrix_response.values

    assert isinstance(enum_items, list), f"crm.enum.{method_name} values should be a list"
    assert enum_items, f"crm.enum.{method_name} values should not be empty"

    for item in enum_items:
        assert isinstance(item, CRMEnumItem), "CRM enum item should be CRMEnumItem"
        assert isinstance(item.bitrix_id, int), "CRMEnumItem.bitrix_id should be an int"
        assert isinstance(item.name, str), "CRMEnumItem.name should be a str"
        assert item.symbol_code is None or isinstance(item.symbol_code, str), "CRMEnumItem.symbol_code should be a str or None"
        assert item.symbol_code_short is None or isinstance(item.symbol_code_short, str), "CRMEnumItem.symbol_code_short should be a str or None"


def test_crm_enum_getorderownertypes(bitrix_client: BaseClient):
    """Test retrieving object types available for order binding."""

    bitrix_response = bitrix_client.crm.enum.getorderownertypes().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)

    owner_types = bitrix_response.values

    assert isinstance(owner_types, list), "Order owner types should be a list"
    assert owner_types, "Order owner types should not be empty"

    for owner_type in owner_types:
        assert isinstance(owner_type, OrderOwnerType), "Order owner type should be OrderOwnerType"
        assert isinstance(owner_type.bitrix_id, int), "OrderOwnerType.bitrix_id should be an int"
        assert isinstance(owner_type.name, str), "OrderOwnerType.name should be a str"
        assert isinstance(owner_type.attribute, str), "OrderOwnerType.attribute should be a str"
        assert isinstance(owner_type.code, str), "OrderOwnerType.code should be a str"
