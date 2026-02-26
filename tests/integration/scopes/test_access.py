from typing import List, Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.access,
]

_ACCESS: List[Text] = ["G2", "AU"]


def test_name(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.access.name(access=_ACCESS).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "Name result should be a dict"

    names = bitrix_response.result

    for access in _ACCESS:
        assert access in names, f"Access {access!r} should be present in result"
        assert isinstance(names[access], dict), f"Value for key {access!r} should be a dictionary"
