from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME
from ._helpers import get_active_open_line_id

pytestmark = [
    pytest.mark.integration,
    pytest.mark.imconnector,
]
_STATUS_FIELDS: Tuple[Text, ...] = ("LINE", "CONNECTOR", "ERROR", "CONFIGURED", "STATUS")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_imconnector_register")
def test_register(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = f"{SDK_NAME.lower()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.imconnector.register(
        bitrix_id=connector_id,
        name=f"{SDK_NAME} Connector",
        icon={"DATA_IMAGE": "https://dev.1c-bitrix.ru/images/main/logo-2x.png"},
        placement_handler="https://example.com/handler",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "imconnector.register result should be dict"

    cache.set("imconnector_id", connector_id)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_imconnector_status", depends=["test_imconnector_register"])
def test_status(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("imconnector_id", None)
    assert isinstance(connector_id, str), "Connector ID should be cached"
    line_id = get_active_open_line_id(bitrix_client)

    bitrix_response = bitrix_client.imconnector.status(
        connector=connector_id,
        line=line_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "imconnector.status result should be a dict"

    status = bitrix_response.result
    for field in _STATUS_FIELDS:
        assert field in status, f"Field '{field}' should be present"

    assert status["CONNECTOR"] == connector_id, "imconnector.status CONNECTOR should match registered connector"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_imconnector_activate", depends=["test_imconnector_status"])
def test_activate(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("imconnector_id", None)
    assert isinstance(connector_id, str), "Connector ID should be cached"
    line_id = get_active_open_line_id(bitrix_client)

    bitrix_response = bitrix_client.imconnector.activate(
        connector=connector_id,
        line=line_id,
        active=True,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (bool, dict)), "imconnector.activate result should be bool or dict"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_imconnector_list", depends=["test_imconnector_activate"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("imconnector_id", None)
    assert isinstance(connector_id, str), "Connector ID should be cached"

    bitrix_response = bitrix_client.imconnector.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "imconnector.list result should be a dict"
    assert connector_id in bitrix_response.result, "Registered connector should be present in imconnector.list"
    assert isinstance(bitrix_response.result[connector_id], str), "imconnector.list connector value should be string"
