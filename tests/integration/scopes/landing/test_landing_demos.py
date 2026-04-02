import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.landing,
    pytest.mark.landing_demos,
]


def test_get_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.demos.get_list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "landing.demos.get_list result should be a list"

    for demo in bitrix_response.result:
        assert isinstance(demo, dict), "Each landing.demos.get_list item should be a dict"
