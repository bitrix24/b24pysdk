import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.pull,
    pytest.mark.pull_application_event,
]


@pytest.mark.oauth_only
def test_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.pull.application.event.add(
        command="SDK_PULL_EVENT",
        params=[{"key": "value"}],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "pull.application.event.add result should be bool"
