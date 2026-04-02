import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.rpa,
    pytest.mark.rpa_type,
]


def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.rpa.type.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "rpa.type.list result should be a dict"

    process_types = bitrix_response.result.get("types")
    assert isinstance(process_types, list), "rpa.type.list result['types'] should be a list"

    for process_type in process_types:
        assert isinstance(process_type, dict), "Each rpa.type.list item should be a dict"
