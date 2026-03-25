from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.lists,
]

_IBLOCK_TYPE_ID: Text = "lists"
_LIST_FIELDS: Tuple[Text, ...] = ("ID", "NAME")


@pytest.mark.dependency(name="test_lists_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = f"sdk_list_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    list_name = f"{SDK_NAME} LIST"

    try:
        bitrix_response = bitrix_client.lists.add(
            iblock_type_id=_IBLOCK_TYPE_ID,
            iblock_code=iblock_code,
            fields={"NAME": list_name},
        ).response
    except BitrixAPIError as error:
        pytest.skip(f"lists.add is unavailable on this portal: {error}")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.add result should be int"
    assert bitrix_response.result > 0, "lists.add should return positive ID"

    cache.set("lists_iblock_id", bitrix_response.result)
    cache.set("lists_iblock_code", iblock_code)


@pytest.mark.dependency(depends=["test_lists_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    bitrix_response = bitrix_client.lists.update(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        fields={"NAME": f"{SDK_NAME} LIST UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.update result should be bool"
    assert bitrix_response.result is True, "lists.update should return True"


@pytest.mark.dependency(depends=["test_lists_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    bitrix_response = bitrix_client.lists.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "lists.get result should be a list"

    iblocks = bitrix_response.result

    assert len(iblocks) == 1, "Expected one list to be returned"

    iblock = iblocks[0]

    assert isinstance(iblock, dict), "List should be a dict"

    for field in _LIST_FIELDS:
        assert field in iblock, f"Field '{field}' should be present"

    assert iblock.get("ID") == str(iblock_id), "List ID should match created list"


@pytest.mark.dependency(depends=["test_lists_add"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    bitrix_response = bitrix_client.lists.delete(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.delete result should be bool"
    assert bitrix_response.result is True, "lists.delete should return True"
