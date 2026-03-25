import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_timecontrol_settings,
]

_FIELDS = (
    "active",
    "minimum_idle_for_report",
    "register_offline",
    "register_idle",
    "register_desktop",
    "report_request_type",
    "report_request_users",
    "report_simple_type",
    "report_simple_users",
    "report_full_type",
    "report_full_users",
)


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.timecontrol.settings.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "timeman.timecontrol.settings.get result should be a dict"

    settings_data = bitrix_response.result

    for field in _FIELDS:
        assert field in settings_data, f"Field '{field}' should be present"


@pytest.mark.oauth_only
def test_set(bitrix_client: BaseClient):
    """"""

    get_response = bitrix_client.timeman.timecontrol.settings.get().response

    assert isinstance(get_response, BitrixAPIResponse)
    assert isinstance(get_response.result, dict), "timeman.timecontrol.settings.get result should be a dict"

    settings_data = get_response.result

    active = settings_data.get("active")
    minimum_idle_for_report = settings_data.get("minimum_idle_for_report")
    register_offline = settings_data.get("register_offline")
    register_idle = settings_data.get("register_idle")
    register_desktop = settings_data.get("register_desktop")
    report_request_type = settings_data.get("report_request_type")
    report_request_users = settings_data.get("report_request_users")
    report_simple_type = settings_data.get("report_simple_type")
    report_simple_users = settings_data.get("report_simple_users")
    report_full_type = settings_data.get("report_full_type")
    report_full_users = settings_data.get("report_full_users")

    bitrix_response = bitrix_client.timeman.timecontrol.settings.set(
        active=active if isinstance(active, bool) else None,
        minimum_idle_for_report=minimum_idle_for_report if isinstance(minimum_idle_for_report, int) else None,
        register_offline=register_offline if isinstance(register_offline, bool) else None,
        register_idle=register_idle if isinstance(register_idle, bool) else None,
        register_desktop=register_desktop if isinstance(register_desktop, bool) else None,
        report_request_type=report_request_type if isinstance(report_request_type, str) else None,
        report_request_users=report_request_users if isinstance(report_request_users, list) else None,
        report_simple_type=report_simple_type if isinstance(report_simple_type, str) else None,
        report_simple_users=report_simple_users if isinstance(report_simple_users, list) else None,
        report_full_type=report_full_type if isinstance(report_full_type, str) else None,
        report_full_users=report_full_users if isinstance(report_full_users, list) else None,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "timeman.timecontrol.settings.set result should be bool"
