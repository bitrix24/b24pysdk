import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.voximplant,
    pytest.mark.voximplant_statistic,
]

_FIELDS = ("ID", "CALL_ID", "PHONE_NUMBER", "CALL_START_DATE", "CALL_TYPE")


def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.voximplant.statistic.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "voximplant.statistic.get result should be a list"

    statistics = bitrix_response.result

    for statistic in statistics:
        assert isinstance(statistic, dict), "Each statistic entry should be a dict"
        for field in _FIELDS:
            assert field in statistic, f"Field '{field}' should be present"
