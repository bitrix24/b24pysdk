from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.client import ClientType
from b24pysdk.objects.department import Department
from b24pysdk.objects.user import User

from ...constants import BITRIX_PORTAL_OWNER_ID, HEAD_DEPARTMENT_ID, SDK_NAME, SORT

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.department,
]

_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SORT", "PARENT", "UF_HEAD")

_NAME: Text = f"{SDK_NAME} DEPARTMENT NAME"
_SORT: int = SORT


@pytest.mark.dependency(name="test_department_fields")
def test_department_fields(bitrix_client: ClientType):
    """"""

    fields = Department.fields.using(client=bitrix_client).list()

    assert isinstance(fields, dict)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], str), f"Field {field!r} should be a string"


@pytest.mark.dependency(name="test_department_add")
def test_department_add(bitrix_client: ClientType, cache: Cache):
    """"""

    parent_department = Department(
        bitrix_pk=HEAD_DEPARTMENT_ID,
        client=bitrix_client,
    )

    head_user = User(
        bitrix_pk=BITRIX_PORTAL_OWNER_ID,
        client=bitrix_client,
    )

    department = Department.objects.using(client=bitrix_client).add(
        name=_NAME,
        parent=parent_department,
        uf_head=head_user,
    )

    assert isinstance(department, Department)
    assert isinstance(department.bitrix_pk, int)

    assert department.bitrix_pk > 0, "Department creation should return a positive ID"

    cache.set("department_id", department.bitrix_pk)


@pytest.mark.dependency(name="test_department_update", depends=["test_department_add"])
def test_department_update(bitrix_client: ClientType, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    department = Department(
        bitrix_pk=department_id,
        client=bitrix_client,
    )

    is_updated = department.update(sort=_SORT)

    assert is_updated is True, "Department update should return True"


@pytest.mark.dependency(name="test_department_get", depends=["test_department_update"])
def test_department_get(bitrix_client: ClientType, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    department = (
        Department.objects
        .using(client=bitrix_client)
        .filter(bitrix_pk=department_id)
        .first()
    )

    assert isinstance(department, Department)
    assert department.bitrix_pk == department_id, "Department ID does not match"
    assert department.name == _NAME, "Department NAME does not match"
    assert department.parent_id == HEAD_DEPARTMENT_ID, "Department PARENT does not match"
    assert department.uf_head_id == BITRIX_PORTAL_OWNER_ID, "Department UF_HEAD does not match"
    assert department.sort == _SORT, "Department SORT does not match"

    uf_head = department.uf_head

    assert isinstance(uf_head, User)
    assert uf_head.bitrix_pk == BITRIX_PORTAL_OWNER_ID


@pytest.mark.dependency(name="test_department_get_as_list", depends=["test_department_update"])
def test_department_get_as_list(bitrix_client: ClientType):
    """"""

    departments = (
        Department.objects
        .using(client=bitrix_client)
        .all()
        .to_list()
    )

    assert isinstance(departments, list)
    assert len(departments) > 1, "Expected at least two departments to be returned"

    for department in departments:
        assert isinstance(department, Department)
        assert isinstance(department.bitrix_pk, int)


@pytest.mark.dependency(name="test_department_get_as_list_fast", depends=["test_department_update"])
def test_department_get_as_list_fast(bitrix_client: ClientType):
    """"""

    departments = (
        Department.objects
        .using(client=bitrix_client)
        .order("-bitrix_pk")
        .as_fast()
    )

    last_department_id = None

    for department in departments:
        assert isinstance(department, Department)

        department_id = department.bitrix_pk

        assert isinstance(department_id, int)

        if last_department_id is not None:
            assert last_department_id > department_id

        last_department_id = department_id


@pytest.mark.dependency(name="test_department_delete", depends=["test_department_add"])
def test_department_delete(bitrix_client: ClientType, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    department = Department(
        bitrix_pk=department_id,
        client=bitrix_client,
    )

    is_deleted = department.delete()

    assert is_deleted is True, "Department deletion should return True"
