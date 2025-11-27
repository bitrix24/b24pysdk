from typing import Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.method,
]

_NAME: Text = "profile"


def test_method_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.method.get(name=_NAME).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "Method get result should be a dict"

    method_data = cast(dict, bitrix_response.result)

    assert method_data.get("isExisting") is True, "Method data field 'isExisting' should return True"
    assert method_data.get("isAvailable") is True, "Method data field 'isAvailable' should return True"
