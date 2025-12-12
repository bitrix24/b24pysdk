from typing import Generator, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse

from ...constants import BITRIX_PORTAL_OWNER_ID, HEAD_DEPARTMENT_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.department,
]

_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SORT", "PARENT", "UF_HEAD")

_NAME: Text = f"{SDK_NAME} DEPARTMENT NAME"
_SORT: int = 123


@pytest.mark.dependency(name="test_department_fields")
def test_department_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.department.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], str), f"Field '{field}' should be a string"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_add")
def test_department_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.department.add(
        name=_NAME,
        parent=HEAD_DEPARTMENT_ID,
        uf_head=BITRIX_PORTAL_OWNER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    department_id = cast(int, bitrix_response.result)

    assert department_id > 0, "Department creation should return a positive ID"

    cache.set("department_id", department_id)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_update", depends=["test_department_add"])
def test_department_update(bitrix_client: Client, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    bitrix_response = bitrix_client.department.update(
        bitrix_id=department_id,
        sort=_SORT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Department update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_get", depends=["test_department_update"])
def test_department_get(bitrix_client: Client, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    bitrix_response = bitrix_client.department.get(bitrix_id=department_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    departments = cast(list, bitrix_response.result)

    assert len(departments) == 1, "Expected one department to be returned"
    department = departments[0]

    assert isinstance(department, dict)

    assert department.get("ID") == str(department_id), "Department ID does not match"
    assert department.get("NAME") == _NAME, "Department NAME does not match"
    assert department.get("PARENT") == str(HEAD_DEPARTMENT_ID), "Department PARENT does not match"
    assert department.get("UF_HEAD") == str(BITRIX_PORTAL_OWNER_ID), "Department UF_HEAD does not match"
    assert department.get("SORT") == _SORT, "Department SORT does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_get_as_list", depends=["test_department_update"])
def test_department_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.department.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    departments = cast(list, bitrix_response.result)

    assert len(departments) > 1, "Expected at least one department to be returned"

    for department in departments:
        assert isinstance(department, dict)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_get_as_list_fast", depends=["test_department_update"])
def test_department_get_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.department.get(sort="ID").as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    departments = cast(Generator, bitrix_response.result)

    last_department_id = None

    for department in departments:
        assert isinstance(department, dict)
        assert "ID" in department

        department_id = int(department["ID"])

        if last_department_id is None:
            last_department_id = department_id
        else:
            assert last_department_id > department_id
            last_department_id = department_id


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_delete", depends=["test_department_get_as_list_fast"])
def test_department_delete(bitrix_client: Client, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    bitrix_response = bitrix_client.department.delete(bitrix_id=department_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Department deletion should return True"
