from typing import cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.access,
]

_KEYS = ["G2", "AU"]


def test_name(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.access.name(access=["G2", "AU"]).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    names = cast(dict, bitrix_response.result)
    assert isinstance(names, dict), "Events should be a dict"

    for key in _KEYS:
        assert key in names, f"Key {key!r} should be present in result"
        assert names[key], f"Value for key {key!r} should not be empty"
