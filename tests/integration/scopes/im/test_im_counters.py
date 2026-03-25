import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
    pytest.mark.im_counters,
]

_FIELDS = ("TYPE", "CHAT", "CHAT_MUTED", "CHAT_UNREAD", "LINES", "DIALOG", "DIALOG_UNREAD")


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.counters.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.counters.get result should be a dict"

    counters_data = bitrix_response.result
    assert len(counters_data) > 0, "im.counters.get result should not be empty"

    for field in _FIELDS:
        assert field in counters_data, f"Field '{field}' should be present"

    for field, value in counters_data.items():
        assert isinstance(field, str), "im.counters.get field names should be strings"
        assert isinstance(value, (int, str, bool, list, dict)), "im.counters.get field value has unexpected type"
