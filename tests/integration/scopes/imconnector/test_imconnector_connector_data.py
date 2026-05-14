import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME
from ._helpers import get_active_open_line_id

pytestmark = [
    pytest.mark.integration,
    pytest.mark.imconnector,
    pytest.mark.imconnector_connector_data,
]


@pytest.mark.oauth_only
def test_set(bitrix_client: BaseClient):
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
        bitrix_response = bitrix_client.imconnector.connector.data.set(
            connector=connector_id,
            line=line_id,
            data={
                "ID": "sdk_chat_1",
                "URL": "https://example.com/chats/sdk_chat_1",
                "NAME": "SDK Chat",
            },
        ).response

        assert isinstance(bitrix_response, BitrixAPIResponse)
        assert isinstance(bitrix_response.result, (bool, dict)), (
            "imconnector.connector.data.set result should be bool or dict"
        )
    finally:
        _ = bitrix_client.imconnector.unregister(bitrix_id=connector_id).response
