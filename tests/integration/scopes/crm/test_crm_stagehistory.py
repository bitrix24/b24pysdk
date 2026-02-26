from typing import Generator, Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants.crm import EntityTypeID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_stagehistory,
]

_FIELDS: Tuple[Text, ...] = ("ID", "TYPE_ID", "OWNER_ID", "CREATED_TIME")
_ENTITY_TYPE_ID: EntityTypeID = EntityTypeID.LEAD


def test_stagehistory_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
        select=list(_FIELDS),
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    assert "items" in result, "Result should contain 'items' key"

    items = result["items"]

    for item in items:
        assert isinstance(item, dict)
        for field in _FIELDS:
            assert field in item, f"Field {field!r} should be present"


def test_stagehistory_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result

    assert len(items) >= 1, "Expected at least one stage history item to be returned"

    for item in items:
        assert isinstance(item, dict)


def test_stagehistory_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
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
