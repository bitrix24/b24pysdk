import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ...constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.mailservice,
]

_MAILSERVICE_TIMEOUT: int = 10
_MAILSERVICE_FIELDS = ("ID", "NAME")


@pytest.mark.oauth_only
def test_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.mailservice.fields(timeout=_MAILSERVICE_TIMEOUT).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "mailservice.fields result should be a dict"

    fields = bitrix_response.result

    assert len(fields) > 0, "mailservice.fields result should not be empty"

    for field, value in fields.items():
        assert isinstance(field, str), "mailservice.fields field names should be strings"
        assert isinstance(value, (dict, str)), "mailservice.fields values should be dict or str"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_mailservice_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    service_name = f"{SDK_NAME} MAIL {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    service_server = "imap.test.local"
    service_port = 993
    service_link = "https://mail.test.local/"

    bitrix_response = bitrix_client.mailservice.add(
        name=service_name,
        encryption=True,
        active=True,
        server=service_server,
        port=service_port,
        link=service_link,
        sort=500,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "mailservice.add should return service ID as int"

    service_id = bitrix_response.result
    assert service_id > 0, "mailservice.add should return a positive ID"

    cache.set("mailservice_id", service_id)
    cache.set("mailservice_name", service_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_mailservice_get", depends=["test_mailservice_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    service_id = cache.get("mailservice_id", None)
    assert isinstance(service_id, int), "mailservice id should be cached"

    service_name = cache.get("mailservice_name", None)
    assert isinstance(service_name, str), "mailservice name should be cached"

    bitrix_response = bitrix_client.mailservice.get(bitrix_id=service_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "mailservice.get result should be a dict"

    service_data = bitrix_response.result
    assert service_data.get("ID") == str(service_id), "mailservice ID does not match"
    assert service_data.get("NAME") == service_name, "mailservice NAME does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_mailservice_list", depends=["test_mailservice_add"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    service_id = cache.get("mailservice_id", None)
    assert isinstance(service_id, int), "mailservice id should be cached"

    bitrix_response = bitrix_client.mailservice.list(timeout=_MAILSERVICE_TIMEOUT).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "mailservice.list result should be a list"

    services = bitrix_response.result

    for service in services:
        assert isinstance(service, dict), "Each mail service should be a dict"

        for field in _MAILSERVICE_FIELDS:
            assert field in service, f"Field '{field}' should be present"

    assert any(service.get("ID") == str(service_id) for service in services), "Created mailservice should be present in list"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_mailservice_update", depends=["test_mailservice_get"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    service_id = cache.get("mailservice_id", None)
    assert isinstance(service_id, int), "mailservice id should be cached"

    updated_name = f"{SDK_NAME} MAIL UPDATED"

    bitrix_response = bitrix_client.mailservice.update(
        bitrix_id=service_id,
        name=updated_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result
    assert is_updated is True, "mailservice.update should return True"

    cache.set("mailservice_name", updated_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_mailservice_delete", depends=["test_mailservice_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    service_id = cache.get("mailservice_id", None)
    assert isinstance(service_id, int), "mailservice id should be cached"

    bitrix_response = bitrix_client.mailservice.delete(bitrix_id=service_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "mailservice.delete should return True"
