from datetime import date, datetime
from typing import Generator, List, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.constants.user import PersonalGender
from b24pysdk.utils.types import JSONDictGenerator

from ....constants import HEAD_DEPARTMENT_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.user,
]

_FIELDS: Tuple[Text, ...] = ("ID", "XML_ID", "ACTIVE", "NAME", "LAST_NAME", "EMAIL", "LAST_LOGIN", "DATE_REGISTER", "TIME_ZONE", "IS_ONLINE", "TIMESTAMP_X",
                             "LAST_ACTIVITY_DATE", "PERSONAL_GENDER", "PERSONAL_BIRTHDAY", "UF_EMPLOYMENT_DATE", "UF_DEPARTMENT")

_NAME: Text = "Test"
_LAST_NAME: Text = SDK_NAME
_UF_DEPARTMENT: List = [HEAD_DEPARTMENT_ID]
_ACTIVE: bool = False
_PERSONAL_GENDER: PersonalGender = PersonalGender.MALE
_PERSONAL_PROFESSION: Text = f"{SDK_NAME}-Developer"
_PERSONAL_BIRTHDAY: date = Config().get_local_date()

_ACCESS: List[Text] = ["AU", "G2"]


def test_user_fields(bitrix_client: Client):
    """Test retrieving user fields and validating the structure."""

    bitrix_response = bitrix_client.user.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], str), f"Field '{field}' should be a string"


@pytest.mark.dependency(name="test_user_add")
def test_user_add(bitrix_client: Client, cache: Cache):
    """Test addition of a new user and validate successful creation."""

    email: Text = f"{int(Config().get_local_datetime().timestamp() * (10 ** 6))}@pysdktest.com"

    bitrix_response = bitrix_client.user.add(
        fields={
            "NAME": _NAME,
            "LAST_NAME": _LAST_NAME,
            "EMAIL": email,
            "UF_DEPARTMENT": _UF_DEPARTMENT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    user_id = cast(int, bitrix_response.result)

    assert user_id > 0, "The result should be a positive integer representing the user ID"

    cache.set("user_id", user_id)
    cache.set("user_email", email)


@pytest.mark.dependency(name="test_user_get", depends=["test_user_add"])
def test_user_get(bitrix_client: Client, cache: Cache):
    """Test retrieving a user by ID."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached after addition"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached after addition"

    bitrix_response = bitrix_client.user.get(
        filter={
            "ID": user_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) == 1, "Expected one user to be returned"
    user = users[0]

    assert isinstance(user, dict)
    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == _NAME, "Name does not match"
    assert user.get("LAST_NAME") == _LAST_NAME, "Last name does not match"
    assert user.get("EMAIL") == user_email, "Email does not match"
    assert user.get("UF_DEPARTMENT") == _UF_DEPARTMENT, "Department does not match"


@pytest.mark.dependency(name="test_user_get_as_list", depends=["test_user_add"])
def test_user_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, dict)


@pytest.mark.dependency(name="test_user_get_as_list_fast", depends=["test_user_add"])
def test_user_get_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    users = cast(JSONDictGenerator, bitrix_response.result)

    last_user_id = None

    for user in users:
        assert isinstance(user, dict)
        assert "ID" in user

        user_id = int(user["ID"])

        if last_user_id is None:
            last_user_id = user_id
        else:
            assert last_user_id > user_id
            last_user_id = user_id


@pytest.mark.dependency(name="test_user_update", depends=["test_user_add"])
def test_user_update(bitrix_client: Client, cache: Cache):
    """Test updating an existing user's attributes."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.user.update(
        fields={
            "ID": user_id,
            "ACTIVE": _ACTIVE,
            "WORK_POSITION": f"{_PERSONAL_PROFESSION} {user_id}",
            "PERSONAL_GENDER": _PERSONAL_GENDER,
            "PERSONAL_PROFESSION": _PERSONAL_PROFESSION,
            "PERSONAL_BIRTHDAY": _PERSONAL_BIRTHDAY.isoformat(),
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "User update should return True"


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search(bitrix_client: Client, cache: Cache):
    """Test searching for users by a given criteria."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached after addition"

    bitrix_response = bitrix_client.user.search(
        filter={
            "FIND": f"{_PERSONAL_PROFESSION} {user_id}",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) == 1, "Expected one user to be returned"

    user = users[0]

    assert isinstance(user, dict)

    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == _NAME, "Name does not match"
    assert user.get("LAST_NAME") == _LAST_NAME, "Last name does not match"
    assert user.get("EMAIL") == user_email, "Email does not match"
    assert user.get("UF_DEPARTMENT") == _UF_DEPARTMENT, "Department does not match"
    assert user.get("ACTIVE") is _ACTIVE, "Activation does not match after update"
    assert user.get("WORK_POSITION") == f"{_PERSONAL_PROFESSION} {user_id}", "User's work position does not match after update"
    assert user.get("PERSONAL_GENDER") == _PERSONAL_GENDER, "User's personal gender does not match after update"
    assert user.get("PERSONAL_PROFESSION") == _PERSONAL_PROFESSION, "User's personal profession does not match after update"
    assert (user.get("PERSONAL_BIRTHDAY") and datetime.fromisoformat(user["PERSONAL_BIRTHDAY"]).date()) == _PERSONAL_BIRTHDAY, "User's personal birthday does not match after update"


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.search().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, dict)


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.search().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    users = cast(JSONDictGenerator, bitrix_response.result)

    last_user_id = None

    for user in users:
        assert isinstance(user, dict)
        assert "ID" in user

        user_id = int(user["ID"])

        if last_user_id is None:
            last_user_id = user_id
        else:
            assert last_user_id > user_id
            last_user_id = user_id


def test_user_current(bitrix_client: Client):
    """Test retrieving details of the current user."""

    bitrix_response = bitrix_client.user.current().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    user = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in user, f"Field '{field}' should be present"
        assert isinstance(user[field], (bool, str, list)), f"Field '{field}' should be a bool, string or list"


def test_user_admin(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.admin().response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_admin = cast(bool, bitrix_response.result)
    assert is_admin is True, "User admin should return True"


def test_user_access(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.access(access=_ACCESS).response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_available = cast(bool, bitrix_response.result)
    assert is_available is True, "User access should return True"
