from typing import List, Text

import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.access import AccessName, AccessNamesDict

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.access,
]

_ACCESS: List[Text] = ["G2", "AU"]


def test_access_name(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.access.name(access=_ACCESS).response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    access_name = bitrix_response.value

    assert isinstance(access_name, AccessNamesDict), "Access name value should be AccessName"

    for access in _ACCESS:
        assert access in access_name, f"Access {access!r} should be present in AccessName"
        assert isinstance(access_name[access], AccessName), f"Value for access {access!r} should be AccessNameItem"
