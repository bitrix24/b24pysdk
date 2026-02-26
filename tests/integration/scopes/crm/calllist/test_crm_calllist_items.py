from typing import List, Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_calllist_items,
]

_LIST_ID: int = 19
_ITEMS_FIELDS: List[Text] = ["ID", "STATUS", "ENTITY_TYPE"]


def test_calllist_items_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.calllist.items.get(
        list_id=_LIST_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result

    assert len(items) >= 1, "Expected at least one item to be returned"

    for item in items:
        assert isinstance(item, dict)
        for field in _ITEMS_FIELDS:
            assert field in item, f"Field {field!r} should be present"
