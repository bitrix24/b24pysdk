from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.status_entity import CRMStatusEntityItem, CRMStatusEntitySemanticInfo, CRMStatusEntityType

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_status,
    pytest.mark.crm_status_entity,
]

_ENTITY_ID: Text = "SOURCE"


def test_crm_status_entity_types(bitrix_client: BaseClient):  # noqa: C901
    """Test retrieving CRM status entity types."""

    bitrix_response = bitrix_client.crm.status.entity.types().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)

    entity_types = bitrix_response.values

    assert isinstance(entity_types, list)
    assert entity_types, "Expected at least one CRM status entity type to be returned"

    for entity_type in entity_types:
        assert isinstance(entity_type, CRMStatusEntityType)
        assert isinstance(entity_type.bitrix_id, str)
        assert isinstance(entity_type.name, str)

        if entity_type.entity_type_id is not None:
            assert isinstance(entity_type.entity_type_id, int)

        if entity_type.semantic_info is not None:
            assert isinstance(entity_type.semantic_info, CRMStatusEntitySemanticInfo)
            assert isinstance(entity_type.semantic_info.start_field, str)
            assert isinstance(entity_type.semantic_info.final_success_field, str)
            assert isinstance(entity_type.semantic_info.final_unsuccess_field, str)
            assert isinstance(entity_type.semantic_info.final_sort, int)

        if entity_type.prefix is not None:
            assert isinstance(entity_type.prefix, str)

        if entity_type.field_attribute_scope is not None:
            assert isinstance(entity_type.field_attribute_scope, str)

        if entity_type.is_enabled is not None:
            assert isinstance(entity_type.is_enabled, bool)

        if entity_type.category_id is not None:
            assert isinstance(entity_type.category_id, int)

        if entity_type.parent_id is not None:
            assert isinstance(entity_type.parent_id, str)

        if entity_type.category_name is not None:
            assert isinstance(entity_type.category_name, str)

        if entity_type.category_sort is not None:
            assert isinstance(entity_type.category_sort, int)

        if entity_type.is_default_category is not None:
            assert isinstance(entity_type.is_default_category, bool)


def test_crm_status_entity_items(bitrix_client: BaseClient):
    """Test retrieving CRM status entity items by entity ID."""

    bitrix_response = bitrix_client.crm.status.entity.items(entity_id=_ENTITY_ID).response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)

    items = bitrix_response.values

    assert isinstance(items, list)
    assert items, "Expected at least one CRM status entity item to be returned"

    for item in items:
        assert isinstance(item, CRMStatusEntityItem)
        assert isinstance(item.name, str)
        assert item.name
        assert isinstance(item.sort, int)
        assert isinstance(item.status_id, str)
        assert item.status_id
