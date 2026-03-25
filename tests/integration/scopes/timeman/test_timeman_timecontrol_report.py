import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_timecontrol_report,
]


@pytest.mark.oauth_only
def test_add(bitrix_client: BaseClient):
    """"""

    now = Config().get_local_datetime()

    reports_response = bitrix_client.timeman.timecontrol.reports.get(
        user_id=BITRIX_PORTAL_OWNER_ID,
        month=now.month,
        year=now.year,
    ).response

    assert isinstance(reports_response, BitrixAPIResponse)
    assert isinstance(reports_response.result, dict), "timeman.timecontrol.reports.get result should be a dict"

    report_data = reports_response.result.get("report", {})
    assert isinstance(report_data, dict), "timeman.timecontrol.reports.get result['report'] should be a dict"

    days = report_data.get("days", [])
    assert isinstance(days, list), "timeman.timecontrol.reports.get result['report']['days'] should be a list"

    report_id = None
    for day in days:
        if not isinstance(day, dict):
            continue

        current_report_id = day.get("REPORT_ID", day.get("report_id"))
        if isinstance(current_report_id, int):
            report_id = current_report_id
            break
        if isinstance(current_report_id, str) and current_report_id.isdigit():
            report_id = int(current_report_id)
            break

    if report_id is None:
        pytest.skip("No REPORT_ID available for timeman.timecontrol.report.add test in current month")

    bitrix_response = bitrix_client.timeman.timecontrol.report.add(
        report_id=report_id,
        text=f"{SDK_NAME} TIMEMAN REPORT",
        type="WORK",
        calendar="N",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "timeman.timecontrol.report.add result should be bool"
    assert bitrix_response.result is True, "timeman.timecontrol.report.add should return True"
