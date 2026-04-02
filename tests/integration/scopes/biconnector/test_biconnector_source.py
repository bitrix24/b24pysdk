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
    pytest.mark.biconnector_source,
]

_FIELDS: Tuple[Text, ...] = ("id", "title")
_SETTINGS_TOKEN: Text = "sdk_test_token"  # noqa: S105
_LOGO: Text = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLz4="


def test_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.source.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.source.fields result should be a dict"


@pytest.mark.dependency(name="test_biconnector_source_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    connector_name = f"{SDK_NAME} CONNECTOR {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    connector_url = "https://httpbin.org/post"

    connector_response = bitrix_client.biconnector.connector.add(
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
    assert isinstance(connector_response, BitrixAPIResponse)
    connector_result = connector_response.result
    if isinstance(connector_result, dict) and "error" in connector_result:
        pytest.fail(f"biconnector.connector.add returned API error payload: {connector_result['error']}")
    connector_id = connector_result.get("id") if isinstance(connector_result, dict) else connector_result
    assert isinstance(connector_id, int), "biconnector.connector.add result id should be int"
    assert connector_id > 0, "biconnector.connector.add should return positive ID"

    source_name = f"{SDK_NAME} SOURCE {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.biconnector.source.add(
        fields={
            "title": source_name,
            "description": f"{SDK_NAME} SOURCE DESCRIPTION",
            "connectorId": connector_id,
            "settings": {
                "token": _SETTINGS_TOKEN,
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    source_result = bitrix_response.result
    if isinstance(source_result, dict) and "error" in source_result:
        pytest.fail(f"biconnector.source.add returned API error payload: {source_result['error']}")
    source_id = source_result.get("id") if isinstance(source_result, dict) else source_result
    assert isinstance(source_id, int), "biconnector.source.add result id should be int"
    assert source_id > 0, "biconnector.source.add should return positive ID"

    cache.set("biconnector_source_id", source_id)
    cache.set("biconnector_source_connector_id", connector_id)


@pytest.mark.dependency(depends=["test_biconnector_source_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    source_id = cache.get("biconnector_source_id", None)
    assert isinstance(source_id, int), "Source ID should be cached"

    bitrix_response = bitrix_client.biconnector.source.get(bitrix_id=source_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.source.get result should be a dict"

    source_result = bitrix_response.result
    source = source_result.get("item") if isinstance(source_result, dict) and "item" in source_result else source_result
    connection = source.get("connection") if isinstance(source, dict) and "connection" in source else source

    assert isinstance(connection, dict), "biconnector.source.get connection should be a dict"
    assert ("id" in connection or "ID" in connection), "Field 'id' should be present"
    assert ("title" in connection or "TITLE" in connection), "Field 'title' should be present"


@pytest.mark.dependency(depends=["test_get"])
def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.source.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    sources_result = bitrix_response.result
    sources = sources_result.get("items", []) if isinstance(sources_result, dict) else sources_result
    assert isinstance(sources, list), "biconnector.source.list result should be a list"

    for source in sources:
        source_item = source.get("item") if isinstance(source, dict) and "item" in source else source
        connection = source_item.get("connection") if isinstance(source_item, dict) and "connection" in source_item else source_item
        assert isinstance(connection, dict), "Each source connection should be a dict"
        assert ("id" in connection or "ID" in connection), "Field 'id' should be present"
        assert ("title" in connection or "TITLE" in connection), "Field 'title' should be present"


@pytest.mark.dependency(depends=["test_list"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    source_id = cache.get("biconnector_source_id", None)
    assert isinstance(source_id, int), "Source ID should be cached"

    bitrix_response = bitrix_client.biconnector.source.update(
        bitrix_id=source_id,
        fields={"title": f"{SDK_NAME} SOURCE UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.source.update result should be bool"
    assert bitrix_response.result is True, "biconnector.source.update should return True"


@pytest.mark.dependency(depends=["test_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    source_id = cache.get("biconnector_source_id", None)
    assert isinstance(source_id, int), "Source ID should be cached"

    bitrix_response = bitrix_client.biconnector.source.delete(bitrix_id=source_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.source.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.source.delete should return True"

    connector_id = cache.get("biconnector_source_connector_id", None)
    assert isinstance(connector_id, int), "Connector ID should be cached"

    bitrix_response = bitrix_client.biconnector.connector.delete(bitrix_id=connector_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.connector.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.connector.delete should return True"
