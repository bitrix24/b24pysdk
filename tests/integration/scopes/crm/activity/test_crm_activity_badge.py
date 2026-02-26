from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import (
    BitrixAPIListResponse,
    BitrixAPIResponse,
)
from b24pysdk.client import BaseClient

from .....constants import SDK_NAME

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_badge,
]

_TITLE: Text = f"{SDK_NAME} Test Badge Title"
_VALUE: Text = f"{SDK_NAME} Test Badge Value"
_TYPE: Text = "failure"


@pytest.mark.dependency(name="test_crm_activity_badge_add")
def test_crm_activity_badge_add(bitrix_client: BaseClient, cache: Cache):
    """Test adding a new badge."""

    code: Text = f"{SDK_NAME.lower()}_test_badge_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.crm.activity.badge.add(
        code=code,
        title=_TITLE,
        value=_VALUE,
        type=_TYPE,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "badge" in result, "Result should contain 'badge' key"

    badge = result["badge"]

    assert isinstance(badge, dict)
    assert badge.get("code") == code, "Badge code does not match"
    assert badge.get("title") == _TITLE, "Badge title does not match"
    assert badge.get("value") == _VALUE, "Badge value does not match"
    assert badge.get("type") == _TYPE, "Badge type does not match"

    cache.set("badge_code", code)


@pytest.mark.dependency(name="test_crm_activity_badge_get", depends=["test_crm_activity_badge_add"])
def test_crm_activity_badge_get(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a badge by code."""

    badge_code = cache.get("badge_code", None)
    assert isinstance(badge_code, str), "Badge code should be cached after addition"

    bitrix_response = bitrix_client.crm.activity.badge.get(code=badge_code).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "badge" in result, "Result should contain 'badge' key"

    badge = result["badge"]

    assert isinstance(badge, dict)
    assert badge.get("code") == badge_code, "Badge code does not match"
    assert badge.get("title") == _TITLE, "Badge title does not match"
    assert badge.get("value") == _VALUE, "Badge value does not match"
    assert badge.get("type") == _TYPE, "Badge type does not match"


@pytest.mark.dependency(name="test_crm_activity_badge_list", depends=["test_crm_activity_badge_get"])
def test_crm_activity_badge_list(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a list of badges."""

    badge_code = cache.get("badge_code", None)
    assert isinstance(badge_code, str), "Badge code should be cached"

    bitrix_response = bitrix_client.crm.activity.badge.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "badges" in result, "Result should contain 'badges' key"

    badges = result["badges"]

    assert isinstance(badges, list)
    assert len(badges) >= 1, "Expected at least one badge to be returned"

    for badge in badges:
        assert isinstance(badge, dict)
        if all((
            badge.get("code") == badge_code,
            badge.get("title") == _TITLE,
            badge.get("value") == _VALUE,
            badge.get("type") == _TYPE,
        )):
            break
    else:
        pytest.fail(f"Test badge with code '{badge_code}' should be found in list")


@pytest.mark.dependency(name="test_crm_activity_badge_list_as_list", depends=["test_crm_activity_badge_list"])
def test_crm_activity_badge_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.activity.badge.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    badges = bitrix_response.result

    assert len(badges) >= 1, "Expected at least one badge to be returned"

    for badge in badges:
        assert isinstance(badge, dict)


@pytest.mark.dependency(name="test_crm_activity_badge_delete", depends=["test_crm_activity_badge_list_as_list"])
def test_crm_activity_badge_delete(bitrix_client: BaseClient, cache: Cache):
    """Test deleting a badge."""

    badge_code = cache.get("badge_code", None)
    assert isinstance(badge_code, str), "Badge code should be cached"

    bitrix_response = bitrix_client.crm.activity.badge.delete(code=badge_code).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result

    assert is_deleted is True, "Badge deletion should return True"
