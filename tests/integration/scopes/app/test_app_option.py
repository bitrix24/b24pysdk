from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.utils.types import JSONDict

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.app,
    pytest.mark.app_option,
]

_OPTION: Text = f"{SDK_NAME}_OPTION"
_OPTION_VALUE: Text = f"{SDK_NAME}_OPTION_VALUE"
_OPTIONS: JSONDict = {
    _OPTION: _OPTION_VALUE,
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_option_set")
def test_option_set(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.app.option.set(
        options=_OPTIONS,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = bitrix_response.result

    assert is_set is True, "Option set should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_option_get", depends=["test_option_set"])
def test_option_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.app.option.get(
        option=_OPTION,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    option_value = bitrix_response.result

    assert option_value == _OPTION_VALUE, "Option value does not match"
