from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.socialnetwork,
    pytest.mark.socialnetwork_api_workgroup,
]

_WORKGROUP_LIST_FIELDS: Tuple[Text, ...] = ("id",)
_WORKGROUP_GET_FIELDS: Tuple[Text, ...] = ("ID", "NAME")


def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.socialnetwork.api.workgroup.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "socialnetwork.api.workgroup.list result should be a dict"

    workgroups = bitrix_response.result.get("workgroups", [])
    assert isinstance(workgroups, list), "socialnetwork.api.workgroup.list result['workgroups'] should be a list"

    if not workgroups:
        pytest.skip("No workgroups available for socialnetwork.api.workgroup.get test")

    workgroup = workgroups[0]

    assert isinstance(workgroup, dict), "Each workgroup should be a dict"

    for field in _WORKGROUP_LIST_FIELDS:
        assert field in workgroup, f"Field '{field}' should be present"


def test_get(bitrix_client: BaseClient):
    """"""

    list_response = bitrix_client.socialnetwork.api.workgroup.list().response

    assert isinstance(list_response, BitrixAPIResponse)
    assert isinstance(list_response.result, dict), "socialnetwork.api.workgroup.list result should be a dict"

    workgroups = list_response.result.get("workgroups", [])
    assert isinstance(workgroups, list), "socialnetwork.api.workgroup.list result['workgroups'] should be a list"

    if not workgroups:
        pytest.skip("No workgroups available for socialnetwork.api.workgroup.get test")

    first_workgroup = workgroups[0]
    assert isinstance(first_workgroup, dict), "Workgroup should be a dict"

    workgroup_id = first_workgroup.get("id")

    if isinstance(workgroup_id, str) and workgroup_id.isdigit():
        workgroup_id = int(workgroup_id)

    assert isinstance(workgroup_id, int), "Workgroup ID should be int"

    bitrix_response = bitrix_client.socialnetwork.api.workgroup.get(params={"groupId": workgroup_id}).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "socialnetwork.api.workgroup.get result should be a dict"

    workgroup = bitrix_response.result

    for field in _WORKGROUP_GET_FIELDS:
        assert field in workgroup, f"Field '{field}' should be present"
