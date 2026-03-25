import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.pull,
    pytest.mark.pull_application_push,
]


@pytest.mark.oauth_only
def test_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.pull.application.push.add(
        user_id=[BITRIX_PORTAL_OWNER_ID],
        text=f"{SDK_NAME} PUSH TEST",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "pull.application.push.add result should be bool"
