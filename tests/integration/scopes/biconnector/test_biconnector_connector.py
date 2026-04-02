from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.biconnector,
    pytest.mark.biconnector_connector,
]

_FIELDS: Tuple[Text, ...] = ("id", "title")
_LOGO: Text = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLz4="


def test_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.connector.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.connector.fields result should be a dict"


@pytest.mark.dependency(name="test_biconnector_connector_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_name = f"{SDK_NAME} CONNECTOR {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    connector_url = "https://httpbin.org/post"

    bitrix_response = bitrix_client.biconnector.connector.add(
        fields={
            "title": connector_name,
            "logo": _LOGO,
            "description": f"{SDK_NAME} CONNECTOR DESCRIPTION",
            "urlCheck": connector_url,
            "urlTableList": connector_url,
            "urlTableDescription": connector_url,
            "urlData": connector_url,
            "settings": [{"name": "Token", "type": "STRING", "code": "token"}],
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    connector_result = bitrix_response.result
    if isinstance(connector_result, dict) and "error" in connector_result:
        pytest.fail(f"biconnector.connector.add returned API error payload: {connector_result['error']}")
    connector_id = connector_result.get("id") if isinstance(connector_result, dict) else connector_result

    assert isinstance(connector_id, int), "biconnector.connector.add result id should be int"
    assert connector_id > 0, "biconnector.connector.add should return positive ID"

    cache.set("biconnector_connector_id", connector_id)


@pytest.mark.dependency(depends=["test_biconnector_connector_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("biconnector_connector_id", None)
    assert isinstance(connector_id, int), "Connector ID should be cached"

    bitrix_response = bitrix_client.biconnector.connector.get(bitrix_id=connector_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.connector.get result should be a dict"

    connector_result = bitrix_response.result
    connector = connector_result.get("item") if isinstance(connector_result, dict) and "item" in connector_result else connector_result

    assert ("id" in connector or "ID" in connector), "Field 'id' should be present"
    assert ("title" in connector or "TITLE" in connector), "Field 'title' should be present"


@pytest.mark.dependency(depends=["test_get"])
def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.connector.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    connectors_result = bitrix_response.result
    connectors = connectors_result.get("items", []) if isinstance(connectors_result, dict) else connectors_result
    assert isinstance(connectors, list), "biconnector.connector.list result should be a list"

    for connector in connectors:
        connector_item = connector.get("item") if isinstance(connector, dict) and "item" in connector else connector
        assert isinstance(connector_item, dict), "Each connector should be a dict"
        assert ("id" in connector_item or "ID" in connector_item), "Field 'id' should be present"
        assert ("title" in connector_item or "TITLE" in connector_item), "Field 'title' should be present"


@pytest.mark.dependency(depends=["test_list"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("biconnector_connector_id", None)
    assert isinstance(connector_id, int), "Connector ID should be cached"

    bitrix_response = bitrix_client.biconnector.connector.update(
        bitrix_id=connector_id,
        fields={"title": f"{SDK_NAME} CONNECTOR UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.connector.update result should be bool"
    assert bitrix_response.result is True, "biconnector.connector.update should return True"


@pytest.mark.dependency(depends=["test_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_id = cache.get("biconnector_connector_id", None)
    assert isinstance(connector_id, int), "Connector ID should be cached"

    bitrix_response = bitrix_client.biconnector.connector.delete(bitrix_id=connector_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.connector.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.connector.delete should return True"
