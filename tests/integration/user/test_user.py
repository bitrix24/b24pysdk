from datetime import datetime
from typing import cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from b24pysdk.constants import DEFAULT_TIMEOUT
from tests.integration.helpers import call_method


@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_fields_real(bitrix_client: Client):
    """Test retrieving user fields and validating the structure."""

    bitrix_response = call_method(bitrix_client, "user.fields", timeout=DEFAULT_TIMEOUT)

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "ID" in result, "Expected 'ID' in user fields"

    for field in ("NAME", "EMAIL", "LAST_NAME"):
        assert field in result, f"Field '{field}' should be present"
        assert isinstance(result[field], str), f"Field '{field}' should be a string"


@pytest.mark.dependency(name="test_user_add_real")
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_add_real(bitrix_client: Client, cache: Cache):
    """Test addition of a new user and validate successful creation."""

    user_add_fields = {
        "NAME": "TEST",
        "LAST_NAME": "B24PYSDK",
        "EMAIL": f"{int(datetime.now().astimezone().timestamp() * (10 ** 6))}@pysdktest.com",
        "UF_DEPARTMENT": [1],
    }

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.add",
        fields=user_add_fields,
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    result = cast(int, bitrix_response.result)
    assert result > 0, "The result should be a positive integer representing the user ID"

    cache.set("user_id", result)


@pytest.mark.dependency(name="test_user_get_real", depends=["test_user_add_real"])
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_get_real(bitrix_client: Client, cache: Cache):
    """Test retrieving a user by ID."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached after addition"

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.get",
        filter={"ID": user_id},
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    result = cast(list, bitrix_response.result)

    assert len(result) == 1, "Expected one user to be returned"
    user = result[0]

    assert isinstance(user, dict)
    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == "TEST", "Name does not match"
    assert user.get("LAST_NAME") == "B24PYSDK", "Last name does not match"


@pytest.mark.dependency(name="test_user_update_real", depends=["test_user_get_real"])
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_update_real(bitrix_client: Client, cache: Cache):
    """Test updating an existing user's attributes."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    update_fields = {
        "ID": user_id,
        "ACTIVE": "N",
        "WORK_POSITION": f"Developer{user_id}",
    }

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.update",
        fields=update_fields,
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    result = bitrix_response.result

    assert result is True, "User update should return True"


@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_webhook_user_current_real(bitrix_client: Client):
    """Test retrieving details of the current user."""

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.current",
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)

    assert "ID" in result

    for field in ("NAME", "EMAIL", "LAST_NAME"):
        assert field in result, f"Field '{field}' should be present"
        assert isinstance(result[field], str), f"Field '{field}' should be a string"


@pytest.mark.dependency(name="test_user_search_real", depends=["test_user_update_real"])
@pytest.mark.integration
@pytest.mark.parametrize("bitrix_client", ["webhook"], indirect=True)
def test_user_search_real(bitrix_client: Client, cache: Cache):
    """Test searching for users by a given criteria."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = call_method(
        client=bitrix_client,
        api_method="user.search",
        filter={"FIND": f"Developer{user_id}"},
        timeout=DEFAULT_TIMEOUT,
    )

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    result = cast(list, bitrix_response.result)

    assert len(result) == 1, "Expected one user to be returned"
    user = result[0]

    assert isinstance(user, dict)
    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == "TEST", "Name does not match"
    assert user.get("LAST_NAME") == "B24PYSDK", "Last name does not match"
    assert user.get("WORK_POSITION") == f"Developer{user_id}", "User's work position does not match after update"
