import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.sonet_group,
    pytest.mark.sonet_group_feature,
]

_FEATURE: str = "blog"
_OPERATION: str = "write_post"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_feature_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_name = f"{SDK_NAME} SONET FEATURE GROUP {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.sonet_group.create(
        ar_fields={
            "NAME": group_name,
            "DESCRIPTION": f"{SDK_NAME} SONET GROUP FEATURE TESTS",
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

    cache.set("sonet_group_feature_group_id", group_id)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_feature_access", depends=["test_sonet_group_feature_prepare"])
def test_access(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_feature_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.feature.access(
        group_id=group_id,
        feature=_FEATURE,
        operation=_OPERATION,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "sonet_group.feature.access result should be bool"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_sonet_group_feature_cleanup", depends=["test_sonet_group_feature_access"])
def test_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    group_id = cache.get("sonet_group_feature_group_id", None)
    assert isinstance(group_id, int), "Group ID should be cached"

    bitrix_response = bitrix_client.sonet_group.delete(group_id=group_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is True, "Group deletion should return True"
