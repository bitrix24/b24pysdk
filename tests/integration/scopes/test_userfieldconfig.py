from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ...constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.userfieldconfig,
]

_LIST_FIELDS = ("id", "fieldName")
_FIELD_WRAPPER_KEY: Text = "field"
_FIELD_FIELDS = ("id", "entityId", "fieldName", "userTypeId")

_MODULE_ID: Text = "crm"
_ENTITY_ID: Text = "CRM_LEAD"
_USER_TYPE_ID: Text = "string"
_MANDATORY: Text = "N"
_SHOW_FILTER: Text = "N"
_EDIT_IN_LIST: Text = "Y"


def test_get_types(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.userfieldconfig.get_types(module_id=_MODULE_ID).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "userfieldconfig.get_types result should be a dict"

    field_types = bitrix_response.result
    assert len(field_types) > 0, "userfieldconfig.get_types result should not be empty"

    for field, value in field_types.items():
        assert isinstance(field, str), "userfieldconfig.get_types field names should be strings"
        assert isinstance(value, (str, dict, list, int, bool)), "userfieldconfig.get_types field value has unexpected type"


def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.userfieldconfig.list(module_id=_MODULE_ID).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "userfieldconfig.list result should be a dict"

    userfieldconfig_data = bitrix_response.result
    assert "fields" in userfieldconfig_data, "Field 'fields' should be present in userfieldconfig.list result"
    assert isinstance(userfieldconfig_data["fields"], list), "Field 'fields' should be a list"

    fields = userfieldconfig_data["fields"]

    for field in fields:
        assert isinstance(field, dict), "Each userfieldconfig item should be a dict"
        for required_field in _LIST_FIELDS:
            assert required_field in field, f"Field '{required_field}' should be present in userfieldconfig item"


@pytest.mark.dependency(name="test_userfieldconfig_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfield_name = f"UF_CRM_LEAD_{SDK_NAME.upper()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"[:50]

    bitrix_response = bitrix_client.userfieldconfig.add(
        module_id=_MODULE_ID,
        field={
            "entityId": _ENTITY_ID,
            "fieldName": userfield_name,
            "userTypeId": _USER_TYPE_ID,
            "mandatory": _MANDATORY,
            "showFilter": _SHOW_FILTER,
            "editInList": _EDIT_IN_LIST,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "userfieldconfig.add result should be a dict"

    added_field = bitrix_response.result.get(_FIELD_WRAPPER_KEY)
    assert isinstance(added_field, dict), "userfieldconfig.add result should contain 'field' dict"

    userfield_id_raw = added_field.get("id")
    assert isinstance(userfield_id_raw, str), "Created userfieldconfig id should be string"

    userfield_id = int(userfield_id_raw)
    assert userfield_id > 0, "userfieldconfig.add should return a positive ID"

    cache.set("userfieldconfig_id", userfield_id)
    cache.set("userfieldconfig_field_name", userfield_name)


@pytest.mark.dependency(name="test_userfieldconfig_get", depends=["test_userfieldconfig_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfieldconfig_id = cache.get("userfieldconfig_id", None)
    assert isinstance(userfieldconfig_id, int), "userfieldconfig id should be cached"

    userfield_name = cache.get("userfieldconfig_field_name", None)
    assert isinstance(userfield_name, str), "userfieldconfig field name should be cached"

    bitrix_response = bitrix_client.userfieldconfig.get(
        module_id=_MODULE_ID,
        bitrix_id=userfieldconfig_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "userfieldconfig.get result should be a dict"

    userfield_data = bitrix_response.result.get(_FIELD_WRAPPER_KEY)
    assert isinstance(userfield_data, dict), "userfieldconfig.get result should contain 'field' dict"

    for field in _FIELD_FIELDS:
        assert field in userfield_data, f"Field '{field}' should be present in userfieldconfig.get result"

    assert userfield_data.get("id") == str(userfieldconfig_id), "userfieldconfig id does not match"
    assert userfield_data.get("entityId") == _ENTITY_ID, "userfieldconfig entityId does not match"
    assert userfield_data.get("fieldName") == userfield_name, "userfieldconfig fieldName does not match"
    assert userfield_data.get("userTypeId") == _USER_TYPE_ID, "userfieldconfig userTypeId does not match"


@pytest.mark.dependency(name="test_userfieldconfig_update", depends=["test_userfieldconfig_get"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfieldconfig_id = cache.get("userfieldconfig_id", None)
    assert isinstance(userfieldconfig_id, int), "userfieldconfig id should be cached"

    edit_form_label = f"{SDK_NAME} Userfieldconfig Label"

    bitrix_response = bitrix_client.userfieldconfig.update(
        module_id=_MODULE_ID,
        bitrix_id=userfieldconfig_id,
        field={
            "mandatory": "Y",
            "editFormLabel": {
                "ru": edit_form_label,
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "userfieldconfig.update result should be a dict"

    updated_field = bitrix_response.result.get(_FIELD_WRAPPER_KEY)
    assert isinstance(updated_field, dict), "userfieldconfig.update result should contain 'field' dict"

    assert updated_field.get("id") == str(userfieldconfig_id), "Updated userfieldconfig id does not match"
    assert updated_field.get("mandatory") == "Y", "Updated userfieldconfig mandatory does not match"


@pytest.mark.dependency(name="test_userfieldconfig_delete", depends=["test_userfieldconfig_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfieldconfig_id = cache.get("userfieldconfig_id", None)
    assert isinstance(userfieldconfig_id, int), "userfieldconfig id should be cached"

    bitrix_response = bitrix_client.userfieldconfig.delete(
        module_id=_MODULE_ID,
        bitrix_id=userfieldconfig_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is None, "userfieldconfig.delete should return None"
