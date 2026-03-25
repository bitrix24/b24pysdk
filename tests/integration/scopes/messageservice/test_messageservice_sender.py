import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.messageservice,
    pytest.mark.messageservice_sender,
]


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_messageservice_sender_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    sender_code = f"sdk_sender_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    sender_name = f"{SDK_NAME} Sender"
    sender_description = f"{SDK_NAME} Sender Description"

    bitrix_response = bitrix_client.messageservice.sender.add(
        code=sender_code,
        type="SMS",
        handler="https://example.com/messageservice/handler",
        name=sender_name,
        description=sender_description,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result is not None, "messageservice.sender.add should return non-empty result"

    cache.set("messageservice_sender_code", sender_code)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_messageservice_sender_get_list", depends=["test_messageservice_sender_add"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    sender_code = cache.get("messageservice_sender_code", None)
    assert isinstance(sender_code, str), "messageservice sender code should be cached"

    bitrix_response = bitrix_client.messageservice.sender.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "messageservice.sender.list result should be a list"

    senders = bitrix_response.result

    for sender in senders:
        assert isinstance(sender, str), "Each sender should be a string code"

    assert sender_code in senders, "Created sender code should be present in sender.list"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_messageservice_sender_update", depends=["test_messageservice_sender_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    sender_code = cache.get("messageservice_sender_code", None)
    assert isinstance(sender_code, str), "messageservice sender code should be cached"

    bitrix_response = bitrix_client.messageservice.sender.update(
        code=sender_code,
        name=f"{SDK_NAME} Sender Updated",
        description=f"{SDK_NAME} Sender Description Updated",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result
    assert is_updated is True, "messageservice.sender.update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_messageservice_sender_delete", depends=["test_messageservice_sender_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    sender_code = cache.get("messageservice_sender_code", None)
    assert isinstance(sender_code, str), "messageservice sender code should be cached"

    bitrix_response = bitrix_client.messageservice.sender.delete(code=sender_code).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "messageservice.sender.delete should return True"
