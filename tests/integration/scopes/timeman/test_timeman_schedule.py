import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_schedule,
]

_FIELDS = ("ID", "NAME", "SCHEDULE_TYPE", "REPORT_PERIOD")


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.schedule.get(bitrix_id=1).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (dict, list)), "timeman.schedule.get result should be dict or list"

    if isinstance(bitrix_response.result, dict):
        schedule_data = bitrix_response.result

        if len(schedule_data) == 0:
            pytest.skip("No timeman schedule with ID=1 found")

        for field in _FIELDS:
            assert field in schedule_data, f"Field '{field}' should be present"
