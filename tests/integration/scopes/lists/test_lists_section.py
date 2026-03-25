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
    pytest.mark.lists_section,
]

_IBLOCK_TYPE_ID = "lists"


@pytest.mark.dependency(name="test_lists_section_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = f"sdk_section_list_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    try:
        bitrix_response = bitrix_client.lists.add(
            iblock_type_id=_IBLOCK_TYPE_ID,
            iblock_code=iblock_code,
            fields={"NAME": f"{SDK_NAME} LIST FOR SECTION"},
        ).response
    except BitrixAPIError as error:
        pytest.skip(f"lists.add is unavailable for lists.section tests: {error}")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.add result should be int"
    assert bitrix_response.result > 0, "lists.add should return positive ID"

    cache.set("lists_section_iblock_id", bitrix_response.result)


@pytest.mark.dependency(name="test_lists_section_add", depends=["test_lists_section_prepare"])
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_section_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    section_code = f"sdk_section_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.lists.section.add(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        section_code=section_code,
        fields={"NAME": f"{SDK_NAME} SECTION"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.section.add result should be int"
    assert bitrix_response.result > 0, "lists.section.add should return positive ID"

    cache.set("lists_section_id", bitrix_response.result)


@pytest.mark.dependency(depends=["test_lists_section_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_section_iblock_id", None)
    section_id = cache.get("lists_section_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.lists.section.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        filter={"ID": section_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "lists.section.get result should be a list"


@pytest.mark.dependency(depends=["test_lists_section_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_section_iblock_id", None)
    section_id = cache.get("lists_section_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.lists.section.update(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        section_id=section_id,
        fields={"NAME": f"{SDK_NAME} SECTION UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.section.update result should be bool"
    assert bitrix_response.result is True, "lists.section.update should return True"


@pytest.mark.dependency(depends=["test_lists_section_add"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_section_iblock_id", None)
    section_id = cache.get("lists_section_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(section_id, int), "Section ID should be cached"

    bitrix_response = bitrix_client.lists.section.delete(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        section_id=section_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.section.delete result should be bool"
    assert bitrix_response.result is True, "lists.section.delete should return True"
