from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.method import MethodGet

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.method,
]

_NAME: Text = "profile"


def test_method_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.method.get(name=_NAME).response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    method_get = bitrix_response.value

    assert isinstance(method_get, MethodGet), "Method get value should be MethodGet"

    assert method_get.is_existing is True, "MethodGet.is_existing should return True"
    assert method_get.is_available is True, "MethodGet.is_available should return True"
