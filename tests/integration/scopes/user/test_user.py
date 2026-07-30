from datetime import date
from typing import List, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import ClientType
from b24pysdk.constants.user import PersonalGender
from b24pysdk.objects.department import Department
from b24pysdk.objects.user import User

from ....constants import HEAD_DEPARTMENT_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.user,
]

_FIELDS: Tuple[Text, ...] = (
    "ID",
    "XML_ID",
    "ACTIVE",
    "NAME",
    "LAST_NAME",
    "EMAIL",
    "LAST_LOGIN",
    "DATE_REGISTER",
    "TIME_ZONE",
    "IS_ONLINE",
    "TIMESTAMP_X",
    "LAST_ACTIVITY_DATE",
    "PERSONAL_GENDER",
    "PERSONAL_BIRTHDAY",
    "UF_EMPLOYMENT_DATE",
    "UF_DEPARTMENT",
)

_NAME: Text = "Test"
_LAST_NAME: Text = SDK_NAME
_UF_DEPARTMENT_IDS: List[int] = [HEAD_DEPARTMENT_ID]
_ACTIVE: bool = False
_PERSONAL_GENDER: PersonalGender = PersonalGender.MALE
_PERSONAL_PROFESSION: Text = f"{SDK_NAME}-Developer"
_PERSONAL_BIRTHDAY: date = Config().get_local_date()

_ACCESS: List[Text] = ["AU", "G2"]


@pytest.mark.dependency(name="test_user_fields")
def test_user_fields(bitrix_client: ClientType):
    """"""

    fields = User.fields.using(client=bitrix_client).list()

    assert isinstance(fields, dict)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], str), f"Field {field!r} should be a string"


@pytest.mark.dependency(name="test_user_add")
def test_user_add(bitrix_client: ClientType, cache: Cache):
    """"""

    email: Text = f"{int(Config().get_local_datetime().timestamp() * (10 ** 6))}@pysdktest.com"

    head_department = Department(
        bitrix_pk=HEAD_DEPARTMENT_ID,
        client=bitrix_client,
    )

    user = User.objects.using(client=bitrix_client).add(
        name=_NAME,
        last_name=_LAST_NAME,
        email=email,
        uf_departments=[head_department],
    )

    assert isinstance(user, User)
    assert isinstance(user.bitrix_pk, int)
    assert user.bitrix_pk > 0, "User creation should return a positive ID"

    cache.set("user_id", user.bitrix_pk)
    cache.set("user_email", email)


@pytest.mark.dependency(name="test_user_update", depends=["test_user_add"])
def test_user_update(bitrix_client: ClientType, cache: Cache):
    """"""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    user = User(
        bitrix_pk=user_id,
        client=bitrix_client,
    )

    is_updated = user.update(
        active=_ACTIVE,
        work_position=f"{_PERSONAL_PROFESSION} {user_id}",
        personal_gender=_PERSONAL_GENDER,
        personal_profession=_PERSONAL_PROFESSION,
        personal_birthday=_PERSONAL_BIRTHDAY,
    )

    assert is_updated is True, "User update should return True"


@pytest.mark.dependency(name="test_user_get", depends=["test_user_update"])
def test_user_get(bitrix_client: ClientType, cache: Cache):
    """"""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached"

    user = (
        User.objects
        .using(client=bitrix_client)
        .filter(bitrix_pk=user_id)
        .admin_mode()
        .first()
    )

    assert isinstance(user, User)
    assert user.bitrix_pk == user_id, "User ID does not match"
    assert user.name == _NAME, "User NAME does not match"
    assert user.last_name == _LAST_NAME, "User LAST_NAME does not match"
    assert user.email == user_email, "User EMAIL does not match"
    assert user.uf_department_ids == _UF_DEPARTMENT_IDS, "User UF_DEPARTMENT does not match"
    assert user.active is _ACTIVE, "User ACTIVE does not match"
    assert user.work_position == f"{_PERSONAL_PROFESSION} {user_id}", "User WORK_POSITION does not match"
    assert user.personal_gender is _PERSONAL_GENDER, "User PERSONAL_GENDER does not match"
    assert user.personal_profession == _PERSONAL_PROFESSION, "User PERSONAL_PROFESSION does not match"
    assert user.personal_birthday == _PERSONAL_BIRTHDAY, "User PERSONAL_BIRTHDAY does not match"

    departments = user.uf_departments

    assert departments is not None
    assert len(departments) == 1
    assert isinstance(departments[0], Department)
    assert departments[0].bitrix_pk == HEAD_DEPARTMENT_ID


@pytest.mark.dependency(name="test_user_get_as_list", depends=["test_user_update"])
def test_user_get_as_list(bitrix_client: ClientType):
    """"""

    users = (
        User.objects
        .using(client=bitrix_client)
        .admin_mode()
        .all()
        .to_list()
    )

    assert isinstance(users, list)
    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, User)
        assert isinstance(user.bitrix_pk, int)


@pytest.mark.dependency(name="test_user_get_as_list_fast", depends=["test_user_update"])
def test_user_get_as_list_fast(bitrix_client: ClientType):
    """"""

    users = (
        User.objects
        .using(client=bitrix_client)
        .admin_mode()
        .order("-bitrix_pk")
        .as_fast()
    )

    last_user_id = None

    for user in users:
        assert isinstance(user, User)

        user_id = user.bitrix_pk

        assert isinstance(user_id, int)

        if last_user_id is not None:
            assert last_user_id > user_id

        last_user_id = user_id


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search(bitrix_client: ClientType, cache: Cache):
    """"""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached"

    user = (
        User.objects
        .using(client=bitrix_client)
        .search(find=f"{_PERSONAL_PROFESSION} {user_id}")
        .admin_mode()
        .first()
    )

    assert isinstance(user, User)
    assert user.bitrix_pk == user_id, "User ID does not match"
    assert user.name == _NAME, "User NAME does not match"
    assert user.last_name == _LAST_NAME, "User LAST_NAME does not match"
    assert user.email == user_email, "User EMAIL does not match"
    assert user.uf_department_ids == _UF_DEPARTMENT_IDS, "User UF_DEPARTMENT does not match"
    assert user.active is _ACTIVE, "User ACTIVE does not match"
    assert user.work_position == f"{_PERSONAL_PROFESSION} {user_id}", "User WORK_POSITION does not match"
    assert user.personal_gender is _PERSONAL_GENDER, "User PERSONAL_GENDER does not match"
    assert user.personal_profession == _PERSONAL_PROFESSION, "User PERSONAL_PROFESSION does not match"
    assert user.personal_birthday == _PERSONAL_BIRTHDAY, "User PERSONAL_BIRTHDAY does not match"


@pytest.mark.dependency(name="test_user_search_as_list", depends=["test_user_update"])
def test_user_search_as_list(bitrix_client: ClientType, cache: Cache):
    """"""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    users = (
        User.objects
        .using(client=bitrix_client)
        .search(name=_NAME)
        .admin_mode()
        .all()
        .to_list()
    )

    assert isinstance(users, list)
    assert len(users) >= 1, "Expected at least one user to be returned"
    assert any(user.bitrix_pk == user_id for user in users)

    for user in users:
        assert isinstance(user, User)
        assert isinstance(user.bitrix_pk, int)


@pytest.mark.dependency(name="test_user_search_as_list_fast", depends=["test_user_update"])
def test_user_search_as_list_fast(bitrix_client: ClientType, cache: Cache):
    """"""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    users = (
        User.objects
        .using(client=bitrix_client)
        .search(last_name=_LAST_NAME)
        .admin_mode()
        .order("-bitrix_pk")
        .as_fast()
    )

    last_user_id = None
    is_created_user_found = False

    for user in users:
        assert isinstance(user, User)

        current_user_id = user.bitrix_pk

        assert isinstance(current_user_id, int)

        if last_user_id is not None:
            assert last_user_id > current_user_id

        if current_user_id == user_id:
            is_created_user_found = True

        last_user_id = current_user_id

    assert is_created_user_found is True, "Created user should be present in search results"


def test_user_current(bitrix_client: ClientType):
    """"""

    user = User.objects.using(client=bitrix_client).current()

    assert isinstance(user, User)
    assert isinstance(user.bitrix_pk, int)
    assert user.bitrix_pk > 0

    bitrix_data = user.bitrix_data

    for field in _FIELDS:
        assert field in bitrix_data, f"Field {field!r} should be present"


def test_user_admin(bitrix_client: ClientType):
    """"""

    bitrix_response = bitrix_client.user.admin().response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_admin = bitrix_response.result
    assert is_admin is True, "User admin should return True"


def test_user_access(bitrix_client: ClientType):
    """"""

    bitrix_response = bitrix_client.user.access(access=_ACCESS).response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_available = bitrix_response.result
    assert is_available is True, "User access should return True"
