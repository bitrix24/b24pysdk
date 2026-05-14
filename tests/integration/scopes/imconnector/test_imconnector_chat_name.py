import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME
from ._helpers import get_active_open_line_id

pytestmark = [
    pytest.mark.integration,
    pytest.mark.imconnector,
    pytest.mark.imconnector_chat_name,
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
        activate_response = bitrix_client.imconnector.activate(
            connector=connector_id,
            line=line_id,
            active=True,
        ).response
        assert isinstance(activate_response, BitrixAPIResponse)
        assert isinstance(activate_response.result, (bool, dict)), "imconnector.activate result should be bool or dict"

        bitrix_response = bitrix_client.imconnector.chat.name.set(
            connector=connector_id,
            line=line_id,
            chat_id="sdk_chat_1",
            name="SDK Chat",
            user_id=str(BITRIX_PORTAL_OWNER_ID),
        ).response

        assert isinstance(bitrix_response, BitrixAPIResponse)
        assert isinstance(bitrix_response.result, (bool, dict)), "imconnector.chat.name.set result should be bool or dict"
    finally:
        _ = bitrix_client.imconnector.unregister(bitrix_id=connector_id).response
