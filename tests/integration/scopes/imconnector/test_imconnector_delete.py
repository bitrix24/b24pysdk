import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME
from ._helpers import get_active_open_line_id

pytestmark = [
    pytest.mark.integration,
    pytest.mark.imconnector,
    pytest.mark.imconnector_delete,
]
_MESSAGES = [
    {
        "user": {"id": "sdk-user-1"},
        "message": {"id": "sdk-message-1"},
        "chat": {"id": "sdk-chat-1"},
    },
]


@pytest.mark.oauth_only
def test_messages(bitrix_client: BaseClient):
    """"""

    connector_id = f"{SDK_NAME.lower()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    register_response = bitrix_client.imconnector.register(
        bitrix_id=connector_id,
        name=f"{SDK_NAME} Connector",
        icon={"DATA_IMAGE": "https://dev.1c-bitrix.ru/images/main/logo-2x.png"},
        placement_handler="https://example.com/handler",
    ).response

    assert isinstance(register_response, BitrixAPIResponse)
    assert isinstance(register_response.result, dict), "imconnector.register result should be dict"
    line_id = get_active_open_line_id(bitrix_client)

    try:
        activate_response = bitrix_client.imconnector.activate(
            connector=connector_id,
            line=line_id,
            active=True,
        ).response
        assert isinstance(activate_response, BitrixAPIResponse)
        assert isinstance(activate_response.result, (bool, dict)), "imconnector.activate result should be bool or dict"

        bitrix_response = bitrix_client.imconnector.delete.messages(
            connector=connector_id,
            line=line_id,
            messages=_MESSAGES,
        ).response

        assert isinstance(bitrix_response, BitrixAPIResponse)
        assert isinstance(bitrix_response.result, (bool, dict)), "imconnector.delete.messages result should be bool or dict"
    finally:
        _ = bitrix_client.imconnector.unregister(bitrix_id=connector_id).response
