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
    pytest.mark.lists_element,
]

_IBLOCK_TYPE_ID = "lists"


@pytest.mark.dependency(name="test_lists_element_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = f"sdk_element_list_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    try:
        bitrix_response = bitrix_client.lists.add(
            iblock_type_id=_IBLOCK_TYPE_ID,
            iblock_code=iblock_code,
            fields={"NAME": f"{SDK_NAME} LIST FOR ELEMENT"},
        ).response
    except BitrixAPIError as error:
        pytest.skip(f"lists.add is unavailable for lists.element tests: {error}")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.add result should be int"
    assert bitrix_response.result > 0, "lists.add should return positive ID"

    iblock_id = bitrix_response.result
    file_field_code = f"SDK_FILE_FIELD_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    field_response = bitrix_client.lists.field.add(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        fields={
            "NAME": f"{SDK_NAME} FILE FIELD",
            "FIELD_NAME": file_field_code,
            "CODE": file_field_code,
            "TYPE": "F",
        },
    ).response

    assert isinstance(field_response, BitrixAPIResponse)
    assert isinstance(field_response.result, str), "lists.field.add result should be string"

    field_id = field_response.result
    assert len(field_id) > 0, "lists.field.add should return non-empty field ID"
    assert field_id.startswith("PROPERTY_"), "lists.field.add should return PROPERTY_* field ID"

    cache.set("lists_element_iblock_id", iblock_id)
    cache.set("lists_element_file_field_id", int(field_id.removeprefix("PROPERTY_")))


@pytest.mark.dependency(name="test_lists_element_add", depends=["test_lists_element_prepare"])
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_element_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    element_code = f"sdk_element_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.lists.element.add(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        element_code=element_code,
        fields={"NAME": f"{SDK_NAME} ELEMENT"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.element.add result should be int"
    assert bitrix_response.result > 0, "lists.element.add should return positive ID"

    cache.set("lists_element_id", bitrix_response.result)


@pytest.mark.dependency(depends=["test_lists_element_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_element_iblock_id", None)
    element_id = cache.get("lists_element_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(element_id, int), "Element ID should be cached"

    bitrix_response = bitrix_client.lists.element.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        element_id=element_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "lists.element.get result should be a list"


@pytest.mark.dependency(depends=["test_lists_element_add"])
def test_get_file_url(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_element_iblock_id", None)
    element_id = cache.get("lists_element_id", None)
    field_id = cache.get("lists_element_file_field_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(element_id, int), "Element ID should be cached"
    assert isinstance(field_id, int), "File field ID should be cached"

    bitrix_response = bitrix_client.lists.element.get.file.url(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        element_id=element_id,
        field_id=field_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "lists.element.get.file.url result should be a list"


@pytest.mark.dependency(depends=["test_lists_element_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_element_iblock_id", None)
    element_id = cache.get("lists_element_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(element_id, int), "Element ID should be cached"

    bitrix_response = bitrix_client.lists.element.update(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        element_id=element_id,
        fields={"NAME": f"{SDK_NAME} ELEMENT UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.element.update result should be bool"
    assert bitrix_response.result is True, "lists.element.update should return True"


@pytest.mark.dependency(depends=["test_lists_element_add"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_element_iblock_id", None)
    element_id = cache.get("lists_element_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(element_id, int), "Element ID should be cached"

    bitrix_response = bitrix_client.lists.element.delete(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        element_id=element_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.element.delete result should be bool"
    assert bitrix_response.result is True, "lists.element.delete should return True"
