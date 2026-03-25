import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import HEAD_DEPARTMENT_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]


def test_department_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.department.get(bitrix_id=[HEAD_DEPARTMENT_ID]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.department.get result should be a list"


def test_department_colleagues_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.department.colleagues.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "im.department.colleagues.list result should be a list"


def test_department_employees_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.department.employees.get(bitrix_id=[HEAD_DEPARTMENT_ID]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.department.employees.get result should be a dict"

    for department_id, users in bitrix_response.result.items():
        assert isinstance(department_id, str), "Department id key should be a string"
        assert isinstance(users, list), "Department users should be a list"


def test_department_managers_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.department.managers.get(bitrix_id=[HEAD_DEPARTMENT_ID]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.department.managers.get result should be a dict"

    for department_id, users in bitrix_response.result.items():
        assert isinstance(department_id, str), "Department id key should be a string"
        assert isinstance(users, list), "Department managers should be a list"
