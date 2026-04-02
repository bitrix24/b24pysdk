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
    pytest.mark.biconnector_dataset,
]

_FIELDS: Tuple[Text, ...] = ("id", "name")
_SETTINGS_TOKEN: Text = "sdk_test_token"  # noqa: S105
_LOGO: Text = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLz4="


def test_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.dataset.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.dataset.fields result should be a dict"


@pytest.mark.dependency(name="test_biconnector_dataset_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    connector_name = f"{SDK_NAME} CONNECTOR {timestamp}"
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

    source_name = f"{SDK_NAME} SOURCE {timestamp}"
    source_response = bitrix_client.biconnector.source.add(
        fields={
            "title": source_name,
            "description": f"{SDK_NAME} SOURCE DESCRIPTION",
            "connectorId": connector_id,
            "settings": {
                "token": _SETTINGS_TOKEN,
            },
        },
    ).response
    assert isinstance(source_response, BitrixAPIResponse)
    source_result = source_response.result
    if isinstance(source_result, dict) and "error" in source_result:
        pytest.fail(f"biconnector.source.add returned API error payload: {source_result['error']}")
    source_id = source_result.get("id") if isinstance(source_result, dict) else source_result
    assert isinstance(source_id, int), "biconnector.source.add result id should be int"
    assert source_id > 0, "biconnector.source.add should return positive ID"

    bitrix_response = bitrix_client.biconnector.dataset.add(
        fields={
            "sourceId": source_id,
            "name": f"sdk_dataset_{timestamp}",
            "externalName": f"{SDK_NAME} DATASET {timestamp}",
            "externalCode": f"sdk_external_{timestamp}",
            "description": f"{SDK_NAME} DATASET DESCRIPTION",
            "fields": [{"type": "string", "name": "SDK_FIELD", "externalCode": "SDK_FIELD"}],
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    dataset_result = bitrix_response.result
    if isinstance(dataset_result, dict) and "error" in dataset_result:
        pytest.fail(f"biconnector.dataset.add returned API error payload: {dataset_result['error']}")
    dataset_id = dataset_result.get("id") if isinstance(dataset_result, dict) else dataset_result
    assert isinstance(dataset_id, int), "biconnector.dataset.add result id should be int"
    assert dataset_id > 0, "biconnector.dataset.add should return positive ID"

    cache.set("biconnector_dataset_id", dataset_id)
    cache.set("biconnector_dataset_source_id", source_id)
    cache.set("biconnector_dataset_connector_id", connector_id)


@pytest.mark.dependency(depends=["test_biconnector_dataset_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    dataset_id = cache.get("biconnector_dataset_id", None)
    assert isinstance(dataset_id, int), "Dataset ID should be cached"

    bitrix_response = bitrix_client.biconnector.dataset.get(bitrix_id=dataset_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "biconnector.dataset.get result should be a dict"

    dataset_result = bitrix_response.result
    dataset = dataset_result.get("item") if isinstance(dataset_result, dict) and "item" in dataset_result else dataset_result

    assert ("id" in dataset or "ID" in dataset), "Field 'id' should be present"
    assert ("name" in dataset or "NAME" in dataset), "Field 'name' should be present"


@pytest.mark.dependency(depends=["test_get"])
def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.biconnector.dataset.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    datasets_result = bitrix_response.result
    datasets = datasets_result.get("items", []) if isinstance(datasets_result, dict) else datasets_result
    assert isinstance(datasets, list), "biconnector.dataset.list result should be a list"

    for dataset in datasets:
        dataset_item = dataset.get("item") if isinstance(dataset, dict) and "item" in dataset else dataset
        assert isinstance(dataset_item, dict), "Each dataset should be a dict"
        assert ("id" in dataset_item or "ID" in dataset_item), "Field 'id' should be present"
        assert ("name" in dataset_item or "NAME" in dataset_item), "Field 'name' should be present"


@pytest.mark.dependency(depends=["test_list"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    dataset_id = cache.get("biconnector_dataset_id", None)
    assert isinstance(dataset_id, int), "Dataset ID should be cached"

    bitrix_response = bitrix_client.biconnector.dataset.update(
        bitrix_id=dataset_id,
        fields={"description": f"{SDK_NAME} DATASET UPDATED"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.dataset.update result should be bool"
    assert bitrix_response.result is True, "biconnector.dataset.update should return True"


@pytest.mark.dependency(depends=["test_update"])
def test_fields_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    dataset_id = cache.get("biconnector_dataset_id", None)
    assert isinstance(dataset_id, int), "Dataset ID should be cached"

    unique_suffix = str(int(Config().get_local_datetime().timestamp() * (10 ** 6)))[-6:]
    field_code = f"SDKF{unique_suffix}"

    bitrix_response = bitrix_client.biconnector.dataset.fields.update(
        bitrix_id=dataset_id,
        add=[{"type": "string", "name": field_code, "externalCode": field_code}],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.dataset.fields_update result should be bool"


@pytest.mark.dependency(depends=["test_fields_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    dataset_id = cache.get("biconnector_dataset_id", None)
    assert isinstance(dataset_id, int), "Dataset ID should be cached"

    bitrix_response = bitrix_client.biconnector.dataset.delete(bitrix_id=dataset_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.dataset.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.dataset.delete should return True"

    source_id = cache.get("biconnector_dataset_source_id", None)
    assert isinstance(source_id, int), "Source ID should be cached"

    bitrix_response = bitrix_client.biconnector.source.delete(bitrix_id=source_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.source.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.source.delete should return True"

    connector_id = cache.get("biconnector_dataset_connector_id", None)
    assert isinstance(connector_id, int), "Connector ID should be cached"

    bitrix_response = bitrix_client.biconnector.connector.delete(bitrix_id=connector_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "biconnector.connector.delete result should be bool"
    assert bitrix_response.result is True, "biconnector.connector.delete should return True"
