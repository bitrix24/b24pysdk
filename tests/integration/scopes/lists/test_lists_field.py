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
    pytest.mark.lists_field,
]

_IBLOCK_TYPE_ID = "lists"
_FIELD_DESCRIPTOR_FIELDS = (
    "FIELD_ID",
    "NAME",
    "TYPE",
    "CODE",
)


@pytest.mark.dependency(name="test_lists_field_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = f"sdk_field_list_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    try:
        bitrix_response = bitrix_client.lists.add(
            iblock_type_id=_IBLOCK_TYPE_ID,
            iblock_code=iblock_code,
            fields={"NAME": f"{SDK_NAME} LIST FOR FIELD"},
        ).response
    except BitrixAPIError as error:
        pytest.skip(f"lists.add is unavailable for lists.field tests: {error}")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "lists.add result should be int"
    assert bitrix_response.result > 0, "lists.add should return positive ID"

    cache.set("lists_field_iblock_id", bitrix_response.result)
    cache.set("lists_field_iblock_code", iblock_code)


@pytest.mark.dependency(name="test_lists_field_add", depends=["test_lists_field_prepare"])
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_field_iblock_id", None)
    assert isinstance(iblock_id, int), "IBlock ID should be cached"

    field_code = f"SDK_FIELD_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.lists.field.add(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        fields={
            "NAME": f"{SDK_NAME} Field",
            "FIELD_NAME": field_code,
            "CODE": field_code,
            "TYPE": "S",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str), "lists.field.add result should be string"
    assert len(bitrix_response.result) > 0, "lists.field.add should return non-empty field code"

    cache.set("lists_field_id", bitrix_response.result)


@pytest.mark.dependency(depends=["test_lists_field_prepare"])
def test_type_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_code = cache.get("lists_field_iblock_code", None)
    assert isinstance(iblock_code, str), "IBlock code should be cached"

    bitrix_response = bitrix_client.lists.field.type.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_code=iblock_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "lists.field.type.get result should be a dict"

    type_map = bitrix_response.result

    for field_type in ("S", "N", "L", "F"):
        assert field_type in type_map, f"Field type '{field_type}' should be present"


@pytest.mark.dependency(depends=["test_lists_field_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_field_iblock_id", None)
    field_id = cache.get("lists_field_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(field_id, str), "Field ID should be cached"

    bitrix_response = bitrix_client.lists.field.get(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        field_id=field_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "lists.field.get result should be a dict"

    field_groups = bitrix_response.result

    assert "S" in field_groups, "Field group 'S' should be present"
    assert isinstance(field_groups["S"], dict), "Field group 'S' should be a dict"

    field_descriptor = field_groups["S"]

    for field in _FIELD_DESCRIPTOR_FIELDS:
        assert field in field_descriptor, f"Field '{field}' should be present"

    assert field_descriptor.get("FIELD_ID") == field_id, "lists.field.get FIELD_ID should match created field"


@pytest.mark.dependency(depends=["test_lists_field_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_field_iblock_id", None)
    field_id = cache.get("lists_field_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(field_id, str), "Field ID should be cached"

    bitrix_response = bitrix_client.lists.field.update(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        field_id=field_id,
        fields={
            "NAME": f"{SDK_NAME} Field Updated",
            "TYPE": "S",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.field.update result should be bool"
    assert bitrix_response.result is True, "lists.field.update should return True"


@pytest.mark.dependency(depends=["test_lists_field_add"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    iblock_id = cache.get("lists_field_iblock_id", None)
    field_id = cache.get("lists_field_id", None)

    assert isinstance(iblock_id, int), "IBlock ID should be cached"
    assert isinstance(field_id, str), "Field ID should be cached"

    bitrix_response = bitrix_client.lists.field.delete(
        iblock_type_id=_IBLOCK_TYPE_ID,
        iblock_id=iblock_id,
        field_id=field_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "lists.field.delete result should be bool"
    assert bitrix_response.result is True, "lists.field.delete should return True"
