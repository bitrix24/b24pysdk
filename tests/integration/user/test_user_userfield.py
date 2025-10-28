from datetime import datetime
from typing import cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from b24pysdk.constants import DEFAULT_TIMEOUT
from tests.integration.helpers import call_method


@pytest.mark.dependency(name="test_user_userfield_add_real")
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_userfield_add_real(bitrix_client: Client, cache: Cache):
    """Test adding a new user field and ensuring the field is created successfully."""

    fields = {
        "FIELD_NAME": f"UF_USR_B24PYSDK_{int(datetime.now().astimezone().timestamp() * (10 ** 6))}",
        "USER_TYPE_ID": "string",
        "MULTIPLE": "Y",
    }

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.userfield.add",
        fields=fields,
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    result = cast(int, bitrix_response.result)

    assert result > 0, "User field creation should return a positive ID"
    cache.set("user_userfield_id", result)


@pytest.mark.dependency(name="test_user_userfield_update_real", depends=["test_user_userfield_add_real"])
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_userfield_update_real(bitrix_client: Client, cache: Cache):
    """Test updating a user field and ensuring updates are successful."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int), "User field ID should be cached"

    fields = {
        "MANDATORY": "Y",
        "SORT": 710,
        "SHOW_IN_LIST": "Y",
    }

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.userfield.update",
        bitrix_id=user_userfield_id,
        fields=fields,
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    result = bitrix_response.result

    assert result is True, "User field update should return True"


@pytest.mark.dependency(name="test_user_userfield_list_real", depends=["test_user_userfield_update_real"])
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_userfield_list_real(bitrix_client: Client, cache: Cache):
    """Test retrieving user fields and ensuring we get the correct fields."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int)

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.userfield.list",
        filter={"ID": user_userfield_id},
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    result = cast(list, bitrix_response.result)

    assert len(result) == 1, "Expected one user field to be returned"

    user_field = result[0]
    assert user_field["ID"] == str(user_userfield_id), "User field ID does not match"


@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_userfield_delete_real(bitrix_client: Client, cache: Cache):
    """Test deleting a specific user field and ensuring the field is removed."""

    user_userfield_id = cache.get("user_userfield_id", None)
    assert isinstance(user_userfield_id, int)

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.userfield.delete",
        bitrix_id=user_userfield_id,
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    result = bitrix_response.result

    assert result is True, "User field deletion should return True"
