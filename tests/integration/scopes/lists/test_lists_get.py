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
    pytest.mark.lists_get,
]

_IBLOCK_TYPE_ID = "lists"


@pytest.mark.dependency(name="test_lists_get_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = f"sdk_get_list_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    try:
        bitrix_response = bitrix_client.lists.add(
            iblock_type_id=_IBLOCK_TYPE_ID,
            iblock_code=iblock_code,
            fields={"NAME": f"{SDK_NAME} LIST FOR GET"},
        ).response
    except BitrixAPIError as error:
        pytest.skip(f"lists.add is unavailable for lists.get tests: {error}")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.add result should be int"
    assert bitrix_response.result > 0, "lists.add should return positive ID"

    cache.set("lists_get_iblock_id", bitrix_response.result)
    cache.set("lists_get_iblock_code", iblock_code)


@pytest.mark.dependency(depends=["test_lists_get_prepare"])
def test_call(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_get_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    bitrix_response = bitrix_client.lists.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "lists.get result should be a list"


@pytest.mark.dependency(depends=["test_lists_get_prepare"])
def test_iblock_type_id(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_get_iblock_id", None)
    iblock_code = cache.get("lists_get_iblock_code", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(iblock_code, str), "IBlock code should be cached"

    bitrix_response = bitrix_client.lists.get.iblock.type.id(
        iblock_id=iblock_id,
        iblock_code=iblock_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str), "lists.get.iblock.type.id result should be string"
    assert len(bitrix_response.result) > 0, "lists.get.iblock.type.id should return non-empty type ID"
