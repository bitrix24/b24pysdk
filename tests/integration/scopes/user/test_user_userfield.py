from datetime import datetime
from typing import Generator, Text, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.constants import B24BoolLit, UserTypeID
from b24pysdk.utils.types import JSONDict

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.user,
    pytest.mark.user_userfield,
]

_USER_TYPE_ID: UserTypeID = UserTypeID.STRING
_MULTIPLE: B24BoolLit = B24BoolLit.TRUE

_XML_ID: Text = "123"
_SORT: Text = "456"
_MANDATORY: B24BoolLit = B24BoolLit.TRUE
_SHOW_FILTER: B24BoolLit = B24BoolLit.TRUE
_SHOW_IN_LIST: B24BoolLit = B24BoolLit.TRUE
_EDIT_IN_LIST: B24BoolLit = B24BoolLit.TRUE
_IS_SEARCHABLE: B24BoolLit = B24BoolLit.TRUE
_SETTINGS_DEFAULT_VALUE: Text = f"{SDK_NAME} SETTINGS DEFAULT VALUE"
_SETTINGS_ROWS: int = 3
_SETTINGS: JSONDict = {
    "DEFAULT_VALUE": _SETTINGS_DEFAULT_VALUE,
    "ROWS": _SETTINGS_ROWS,
}


@pytest.mark.dependency(name="test_user_userfield_add")
def test_user_userfield_add(bitrix_client: Client, cache: Cache):
    """Test adding a new user field and ensuring the field is created successfully."""

    user_userfield_field_name = f"UF_USR_B24PYSDK_{int(datetime.now(tz=Config().tzinfo).timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.user.userfield.add(
        fields={
            "FIELD_NAME": user_userfield_field_name,
            "USER_TYPE_ID": _USER_TYPE_ID,
            "MULTIPLE": _MULTIPLE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    user_userfield_id = cast(int, bitrix_response.result)

    assert user_userfield_id > 0, "User field creation should return a positive ID"

    cache.set("user_userfield_id", user_userfield_id)
    cache.set("user_userfield_field_name", user_userfield_field_name)


@pytest.mark.dependency(name="test_user_userfield_update", depends=["test_user_userfield_add"])
def test_user_userfield_update(bitrix_client: Client, cache: Cache):
    """Test updating a user field and ensuring updates are successful."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int), "User field ID should be cached"

    bitrix_response = bitrix_client.user.userfield.update(
        bitrix_id=user_userfield_id,
        fields={
            "XML_ID": _XML_ID,
            "SORT": _SORT,
            # "MANDATORY": _MANDATORY,
            # "SHOW_FILTER": _SHOW_FILTER,
            "SHOW_IN_LIST": _SHOW_IN_LIST,
            "EDIT_IN_LIST": _EDIT_IN_LIST,
            # "IS_SEARCHABLE": _IS_SEARCHABLE,
            "SETTINGS": _SETTINGS,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "User field update should return True"


@pytest.mark.dependency(name="test_user_userfield_list", depends=["test_user_userfield_update"])
def test_user_userfield_list(bitrix_client: Client, cache: Cache):
    """Test retrieving user fields and ensuring we get the correct fields."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int)

    user_userfield_field_name = cache.get("user_userfield_field_name", None)
    assert isinstance(user_userfield_field_name, str)

    bitrix_response = bitrix_client.user.userfield.list(
        filter={
            "ID": user_userfield_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    user_userfields = cast(list, bitrix_response.result)

    assert len(user_userfields) == 1, "Expected one user field to be returned"

    user_userfield = user_userfields[0]

    assert isinstance(user_userfield, dict)

    assert user_userfield.get("ID") == str(user_userfield_id), "User userfield ID does not match"
    assert user_userfield.get("FIELD_NAME") == user_userfield_field_name, "User userfield FIELD_NAME does not match"
    assert user_userfield.get("USER_TYPE_ID") == _USER_TYPE_ID, "User userfield USER_TYPE_ID does not match"
    assert user_userfield.get("MULTIPLE") == _MULTIPLE, "User userfield MULTIPLE does not match"
    assert user_userfield.get("XML_ID") == _XML_ID, "User userfield XML_ID does not match"
    assert user_userfield.get("SORT") == _SORT, "User userfield SORT does not match"
    # assert user_field.get("MANDATORY") == _MANDATORY, "User field MANDATORY does not match"
    # assert user_userfield.get("SHOW_FILTER") == _SHOW_FILTER, "User userfield SHOW_FILTER does not match"
    assert user_userfield.get("SHOW_IN_LIST") == _SHOW_IN_LIST, "User userfield SHOW_IN_LIST does not match"
    assert user_userfield.get("EDIT_IN_LIST") == _EDIT_IN_LIST, "User userfield EDIT_IN_LIST does not match"
    # assert user_userfield.get("IS_SEARCHABLE") == _IS_SEARCHABLE, "User userfield IS_SEARCHABLE does not match"

    assert isinstance(user_userfield.get("SETTINGS"), dict), "User userfield SETTINGS is not a dictionary"

    user_userfield_settings = cast(dict, user_userfield["SETTINGS"])

    assert user_userfield_settings.get("DEFAULT_VALUE") == _SETTINGS_DEFAULT_VALUE, "User userfield SETTINGS DEFAULT_VALUE does not match"
    assert user_userfield_settings.get("ROWS") == _SETTINGS_ROWS, "User userfield SETTINGS ROWS does not match"


@pytest.mark.dependency(name="test_user_userfield_list_as_list", depends=["test_user_userfield_update"])
def test_user_userfield_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.userfield.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    user_userfields = cast(list, bitrix_response.result)

    assert len(user_userfields) >= 1, "Expected at least one user userfield to be returned"

    for user_userfield in user_userfields:
        assert isinstance(user_userfield, dict)


@pytest.mark.dependency(name="test_user_userfield_list_as_list_fast", depends=["test_user_userfield_update"])
def test_user_userfield_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.userfield.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    user_userfields = cast(Generator[list, None, None], bitrix_response.result)

    last_user_userfield_id = None

    for user_userfield in user_userfields:
        assert isinstance(user_userfield, dict)
        assert "ID" in user_userfield

        user_userfield_id = int(user_userfield["ID"])

        if last_user_userfield_id is None:
            last_user_userfield_id = user_userfield_id
        else:
            assert last_user_userfield_id > user_userfield_id
            last_user_userfield_id = user_userfield_id


@pytest.mark.dependency(name="test_user_userfield_delete", depends=["test_user_userfield_add"])
def test_user_userfield_delete(bitrix_client: Client, cache: Cache):
    """Test deleting a specific user field and ensuring the field is removed."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int)

    bitrix_response = bitrix_client.user.userfield.delete(
        bitrix_id=user_userfield_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "User field deletion should return True"
