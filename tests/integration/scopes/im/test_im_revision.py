import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
    pytest.mark.im_revision,
]

_FIELDS = ("rest", "web", "mobile")


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.im.revision.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.revision.get result should be a dict"

    revision_data = bitrix_response.result
    assert len(revision_data) > 0, "im.revision.get result should not be empty"

    for field in _FIELDS:
        assert field in revision_data, f"Field '{field}' should be present"

    for field, value in revision_data.items():
        assert isinstance(field, str), "im.revision.get field names should be strings"
        assert isinstance(value, (int, str, bool, list, dict)), "im.revision.get field value has unexpected type"
