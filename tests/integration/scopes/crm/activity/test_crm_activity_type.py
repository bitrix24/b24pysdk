from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import (
    BitrixAPIResponse,
)
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit

from .....constants import SDK_NAME

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_type,
]

_TYPE_ID: Text = f"{SDK_NAME.upper()}_ACTIVITY_TYPE_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
_NAME: Text = f"{SDK_NAME} Custom Activity Type"
_IS_CONFIGURABLE_TYPE: B24BoolLit = B24BoolLit.TRUE


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_type_add")
def test_crm_activity_type_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.activity.type.add(
        fields={
            "TYPE_ID": _TYPE_ID,
            "NAME": _NAME,
            "IS_CONFIGURABLE_TYPE": _IS_CONFIGURABLE_TYPE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    assert result is True

    cache.set("activity_type_id", _TYPE_ID)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_type_list", depends=["test_crm_activity_type_add"])
def test_crm_activity_type_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    activity_type_id = cache.get("activity_type_id", None)
    assert isinstance(activity_type_id, Text)

    bitrix_response = bitrix_client.crm.activity.type.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    activity_types = bitrix_response.result

    for activity_type in activity_types:
        assert isinstance(activity_type, dict)
        if all((
            activity_type.get("TYPE_ID") == activity_type_id,
            activity_type.get("NAME") == _NAME,
            activity_type.get("IS_CONFIGURABLE_TYPE") == _IS_CONFIGURABLE_TYPE,
        )):
            break
    else:
        pytest.fail(f"Test activity type with TYPE_ID {activity_type_id} should be found in list")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_type_delete", depends=["test_crm_activity_type_list"])
def test_crm_activity_type_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    activity_type_id = cache.get("activity_type_id", None)
    assert isinstance(activity_type_id, Text)

    bitrix_response = bitrix_client.crm.activity.type.delete(
        type_id=activity_type_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is True
