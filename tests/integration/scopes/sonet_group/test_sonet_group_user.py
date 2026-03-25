import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants.sonet_group import SonetGroupMemberRole

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.sonet_group,
    pytest.mark.sonet_group_user,
]

_SONET_GROUP_USER_TIMEOUT: int = 10
_MODERATOR_ROLE: SonetGroupMemberRole = SonetGroupMemberRole.MODERATOR
_GROUP_FIELDS = ("GROUP_ID", "GROUP_NAME", "ROLE")
_USER_FIELDS = ("USER_ID", "ROLE")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_name = f"{SDK_NAME} SONET USER GROUP {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.sonet_group.create(
        ar_fields={
            "NAME": group_name,
            "DESCRIPTION": f"{SDK_NAME} SONET GROUP USER TESTS",
            "VISIBLE": "Y",
            "OPENED": "Y",
            "INITIATE_PERMS": "A",
            "SPAM_PERMS": "A",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    group_id = bitrix_response.result
    assert group_id > 0, "Group creation should return a positive ID"

    cache.set("sonet_group_user_group_id", group_id)
    cache.set("sonet_group_user_id", BITRIX_PORTAL_OWNER_ID)


@pytest.mark.oauth_only
def test_groups(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.sonet_group.user.groups(timeout=_SONET_GROUP_USER_TIMEOUT).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    groups = bitrix_response.result
    for group in groups:
        assert isinstance(group, dict)
        for field in _GROUP_FIELDS:
            assert field in group, f"Field '{field}' should be present"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_get", depends=["test_sonet_group_user_prepare"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.get(bitrix_id=group_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    users = bitrix_response.result
    for user in users:
        assert isinstance(user, dict)
        for field in _USER_FIELDS:
            assert field in user, f"Field '{field}' should be present"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_request", depends=["test_sonet_group_user_prepare"])
def test_request(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.request(group_id=group_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is True or isinstance(bitrix_response.result, str)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_invite", depends=["test_sonet_group_user_prepare"])
def test_invite(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    user_id = cache.get("sonet_group_user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.invite(
        group_id=group_id,
        user_id=user_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_add", depends=["test_sonet_group_user_prepare"])
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    user_id = cache.get("sonet_group_user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.add(
        group_id=group_id,
        user_id=user_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "Operation result should be a list of affected user IDs"

    for result_user_id in bitrix_response.result:
        assert isinstance(result_user_id, str), "Affected user ID should be a string"
        assert result_user_id.isdigit(), "Affected user ID should contain only digits"
        assert int(result_user_id) > 0, "Affected user ID should be a positive integer"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_update", depends=["test_sonet_group_user_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    user_id = cache.get("sonet_group_user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.update(
        group_id=group_id,
        user_id=user_id,
        role=_MODERATOR_ROLE,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "Operation result should be a list of affected user IDs"

    for result_user_id in bitrix_response.result:
        assert isinstance(result_user_id, str), "Affected user ID should be a string"
        assert result_user_id.isdigit(), "Affected user ID should contain only digits"
        assert int(result_user_id) > 0, "Affected user ID should be a positive integer"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_delete", depends=["test_sonet_group_user_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    user_id = cache.get("sonet_group_user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.sonet_group.user.delete(
        group_id=group_id,
        user_id=user_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "Operation result should be a list of affected user IDs"

    for result_user_id in bitrix_response.result:
        assert isinstance(result_user_id, str), "Affected user ID should be a string"
        assert result_user_id.isdigit(), "Affected user ID should contain only digits"
        assert int(result_user_id) > 0, "Affected user ID should be a positive integer"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_user_cleanup", depends=["test_sonet_group_user_delete"])
def test_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_user_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.delete(group_id=group_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is True, "Group deletion should return True"
