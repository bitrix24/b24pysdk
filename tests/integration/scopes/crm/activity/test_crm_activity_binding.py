from typing import cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_binding,
]

_ACTIVITY_ID: int = 1
_ENTITY_TYPE_ID: int = 2
_ENTITY_ID: int = 1
_TARGET_ENTITY_ID: int = 2


@pytest.mark.dependency(name="test_crm_activity_binding_add")
def test_crm_activity_binding_add(bitrix_client: Client):
    """Test adding a binding to a CRM entity."""

    bitrix_response = bitrix_client.crm.activity.binding.add(
        activity_id=_ACTIVITY_ID,
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_ENTITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_added = cast(bool, bitrix_response.result)

    assert is_added is True, "Binding addition should return True"


@pytest.mark.dependency(name="test_crm_activity_binding_list", depends=["test_crm_activity_binding_add"])
def test_crm_activity_binding_list(bitrix_client: Client):
    """Test retrieving a list of bindings for an activity."""

    bitrix_response = bitrix_client.crm.activity.binding.list(
        activity_id=_ACTIVITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    bindings = cast(list, bitrix_response.result)

    assert len(bindings) >= 1, "Expected at least one binding to be returned"

    for binding in bindings:
        assert isinstance(binding, dict)
        if all((
            binding.get("entityTypeId") == _ENTITY_TYPE_ID,
            binding.get("entityId") == _ENTITY_ID,
        )):
            break
    else:
        pytest.fail("Test binding should be found in list")


@pytest.mark.dependency(name="test_crm_activity_binding_move", depends=["test_crm_activity_binding_list"])
def test_crm_activity_binding_move(bitrix_client: Client):
    """Test updating a binding to a different CRM entity."""

    bitrix_response = bitrix_client.crm.activity.binding.move(
        activity_id=_ACTIVITY_ID,
        source_entity_type_id=_ENTITY_TYPE_ID,
        source_entity_id=_ENTITY_ID,
        target_entity_type_id=_ENTITY_TYPE_ID,
        target_entity_id=_TARGET_ENTITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_moved = cast(bool, bitrix_response.result)

    assert is_moved is True, "Binding move should return True"


@pytest.mark.dependency(name="test_crm_activity_binding_delete", depends=["test_crm_activity_binding_move"])
def test_crm_activity_binding_delete(bitrix_client: Client):
    """Test deleting a binding from a CRM entity."""

    bitrix_response = bitrix_client.crm.activity.binding.delete(
        activity_id=_ACTIVITY_ID,
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_TARGET_ENTITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Binding deletion should return True"
