import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.profile import Profile

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.profile,
]


def test_profile(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.profile().response
    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    profile = bitrix_response.value
    assert isinstance(profile, Profile), "User profile should be Profile"
