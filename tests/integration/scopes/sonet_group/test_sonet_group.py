from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.sonet_group,
]

_DESCRIPTION: Text = f"{SDK_NAME} SONET GROUP DESCRIPTION"
_GROUP_FIELDS = ("ID", "NAME")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_create")
def test_create(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_name = f"{SDK_NAME} SONET GROUP {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.sonet_group.create(
        ar_fields={
            "NAME": group_name,
            "DESCRIPTION": _DESCRIPTION,
            "VISIBLE": "Y",
            "OPENED": "Y",
            "LANDING": "N",
            "INITIATE_PERMS": "A",
            "SPAM_PERMS": "A",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    group_id = bitrix_response.result
    assert group_id > 0, "Group creation should return a positive ID"

    cache.set("sonet_group_id", group_id)
    cache.set("sonet_group_name", group_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_get", depends=["test_sonet_group_create"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    group_name = cache.get("sonet_group_name", None)
    assert isinstance(group_name, str), "Group NAME should be cached"

    bitrix_response = bitrix_client.sonet_group.get(
        filter={"ID": group_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    groups = bitrix_response.result
    assert len(groups) == 1, "Expected one group to be returned"

    group = groups[0]
    assert isinstance(group, dict)
    for field in _GROUP_FIELDS:
        assert field in group, f"Field '{field}' should be present"

    assert group.get("ID") == str(group_id), "Group ID does not match"
    assert group.get("NAME") == group_name, "Group NAME does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_update", depends=["test_sonet_group_get"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    updated_name = f"{SDK_NAME} SONET GROUP UPDATED"

    bitrix_response = bitrix_client.sonet_group.update(
        group_id=group_id,
        name=updated_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)
    assert bitrix_response.result == group_id, "Updated group ID should match"

    cache.set("sonet_group_name", updated_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_setowner", depends=["test_sonet_group_update"])
def test_setowner(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.setowner(
        group_id=group_id,
        user_id=BITRIX_PORTAL_OWNER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is True, "setowner should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_delete", depends=["test_sonet_group_setowner"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.delete(group_id=group_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is True, "Group deletion should return True"
