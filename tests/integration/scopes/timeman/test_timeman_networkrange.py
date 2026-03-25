from typing import TYPE_CHECKING, List

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

if TYPE_CHECKING:
    from b24pysdk.utils.types import JSONDict

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
    pytest.mark.timeman_networkrange,
]

_NETWORK_RANGE_FIELDS = ("IP_RANGE", "NAME")
_NETWORK_RANGE_FIELDS_LOWER = ("ip_range", "name")
_NETWORK_RANGE_CHECK_FIELDS = ("ip", "range", "name")


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.networkrange.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "timeman.networkrange.get result should be a list"

    ranges = bitrix_response.result

    for range_data in ranges:
        assert isinstance(range_data, dict), "Each network range should be a dict"
        assert (
            all(field in range_data for field in _NETWORK_RANGE_FIELDS)
            or all(field in range_data for field in _NETWORK_RANGE_FIELDS_LOWER)
        ), "Each network range should contain required fields"

@pytest.mark.oauth_only
def test_set(bitrix_client: BaseClient):
    """"""

    get_response = bitrix_client.timeman.networkrange.get().response

    assert isinstance(get_response, BitrixAPIResponse)
    assert isinstance(get_response.result, list), "timeman.networkrange.get result should be a list"

    ranges = get_response.result

    api_ranges: List["JSONDict"] = []

    for range_data in ranges:
        assert isinstance(range_data, dict), "Each network range should be a dict"

        ip_range = range_data.get("IP_RANGE", range_data.get("ip_range"))
        name = range_data.get("NAME", range_data.get("name"))

        if isinstance(ip_range, str) and isinstance(name, str):
            api_ranges.append(
                {
                    "ip_range": ip_range,
                    "name": name,
                },
            )

    if len(api_ranges) == 0:
        api_ranges = [
            {
                "ip_range": "10.0.0.0-10.255.255.255",
                "name": "SDK Office Network",
            },
        ]

    bitrix_response = bitrix_client.timeman.networkrange.set(ranges=api_ranges).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (bool, dict)), "timeman.networkrange.set result should be bool or dict"

    if isinstance(bitrix_response.result, dict):
        assert "result" in bitrix_response.result, "Field 'result' should be present"
        assert isinstance(bitrix_response.result["result"], bool), "Nested 'result' should be bool"


@pytest.mark.oauth_only
def test_check(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.networkrange.check().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is False or isinstance(bitrix_response.result, dict), "timeman.networkrange.check result should be False or dict"

    if isinstance(bitrix_response.result, dict):
        check_data = bitrix_response.result
        for field in _NETWORK_RANGE_CHECK_FIELDS:
            assert field in check_data, f"Field '{field}' should be present"
