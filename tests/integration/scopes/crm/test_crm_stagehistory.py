from typing import Generator, Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.utils.types import JSONDictGenerator

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_stagehistory,
]

_ENTITY_TYPE_ID: int = 2
_FIELDS: Tuple[Text, ...] = (
"ID", "TYPE_ID", "OWNER_ID", "CREATED_TIME", "CATEGORY_ID", "STAGE_SEMANTIC_ID", "STAGE_ID")


def test_stagehistory_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
        select=["ID", "TYPE_ID", "OWNER_ID", "CREATED_TIME", "CATEGORY_ID", "STAGE_SEMANTIC_ID", "STAGE_ID"],
        order={"ID": "ASC"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "items" in result, "Result should contain 'items' key"

    items = cast(list, result["items"])

    for item in items:
        assert isinstance(item, dict)
        for field in _FIELDS:
            assert field in item, f"Field {field!r} should be present"


@pytest.mark.dependency(name="test_stagehistory_list_as_list", depends=[])
def test_stagehistory_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    items = cast(list, bitrix_response.result)

    assert len(items) >= 1, "Expected at least one stage history item to be returned"

    for item in items:
        assert isinstance(item, dict)


@pytest.mark.dependency(name="test_stagehistory_list_as_list_fast", depends=[])
def test_stagehistory_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.stagehistory.list(
        entity_type_id=_ENTITY_TYPE_ID,
    ).as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    items = cast(JSONDictGenerator, bitrix_response.result)

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
