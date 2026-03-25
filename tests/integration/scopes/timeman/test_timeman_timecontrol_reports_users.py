import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_timecontrol_reports_users,
]

_FIELDS = (
    "id",
    "name",
    "first_name",
    "last_name",
    "work_position",
    "avatar",
    "personal_gender",
    "last_activity_date",
)


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.timecontrol.reports.users.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "timeman.timecontrol.reports.users.get result should be a list"

    users = bitrix_response.result

    for user in users:
        assert isinstance(user, dict), "Each user should be a dict"

        for field in _FIELDS:
            assert field in user, f"Field '{field}' should be present"
