from typing import Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.department,
]

# _DEPARTMENT_NAME = "TestDeptSDK"
# _UPDATED_DEPARTMENT_NAME = "TestDeptSDKUpdated"
# _PARENT_ID = 1
_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SORT", "PARENT", "UF_HEAD")

# @pytest.mark.oauth_only
# @pytest.mark.dependency(name="test_department_add")
# def test_department_add(bitrix_client: Client, cache):
#     resp = bitrix_client.department.add(
#         name=_DEPARTMENT_NAME,
#         parent=_PARENT_ID,
#     )
#     response = resp.response
#     assert isinstance(response, BitrixAPIResponse)
#     assert isinstance(response.result, int)
#     cache.set("department_id", response.result)
#
#
# @pytest.mark.oauth_only
# @pytest.mark.dependency(name="test_department_get", depends=["test_department_add"])
# def test_department_get(bitrix_client: Client, cache):
#     department_id = cache.get("department_id", None)
#     assert isinstance(department_id, int)
#     resp = bitrix_client.department.get(bitrix_id=department_id)
#     response = resp.response
#     assert isinstance(response, BitrixAPIResponse)
#     assert isinstance(response.result, list)
#     assert any(str(dep["ID"]) == str(department_id) for dep in response.result)
#
#
# @pytest.mark.oauth_only
# @pytest.mark.dependency(name="test_department_update", depends=["test_department_add"])
# def test_department_update(bitrix_client: Client, cache):
#     department_id = cache.get("department_id", None)
#     assert isinstance(department_id, int)
#     resp = bitrix_client.department.update(
#         bitrix_id=department_id,
#         name=_UPDATED_DEPARTMENT_NAME,
#     )
#     response = resp.response
#     assert isinstance(response, BitrixAPIResponse)
#
#
# @pytest.mark.oauth_only
# @pytest.mark.dependency(name="test_department_delete", depends=["test_department_add"])
# def test_department_delete(bitrix_client: Client, cache):
#     department_id = cache.get("department_id", None)
#     assert isinstance(department_id, int)
#     resp = bitrix_client.department.delete(bitrix_id=department_id)
#     response = resp.response
#     assert isinstance(response, BitrixAPIResponse)


def test_department_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.department.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
