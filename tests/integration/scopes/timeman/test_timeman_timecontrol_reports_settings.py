import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_timecontrol_reports_settings,
]

_FIELDS = (
    "active",
    "user_id",
    "user_admin",
    "user_head",
    "departments",
    "minimum_idle_for_report",
    "report_view_type",
)


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.timecontrol.reports.settings.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "timeman.timecontrol.reports.settings.get result should be a dict"

    reports_settings_data = bitrix_response.result

    for field in _FIELDS:
        assert field in reports_settings_data, f"Field '{field}' should be present"
