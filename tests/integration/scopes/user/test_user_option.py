from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.utils.types import JSONDict

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.user,
    pytest.mark.user_option,
]

_OPTION: Text = f"{SDK_NAME}_OPTION"
_OPTION_VALUE: Text = f"{SDK_NAME}_OPTION_VALUE"
_OPTIONS: JSONDict = {
    _OPTION: _OPTION_VALUE,
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_user_option_set")
def test_user_option_set(bitrix_client: BaseClient):
    """Test adding a new user option and ensuring it is created successfully."""

    bitrix_response = bitrix_client.user.option.set(
        options=_OPTIONS,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = bitrix_response.result

    assert is_set is True, "User option set should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_user_option_get", depends=["test_user_option_set"])
def test_user_option_get(bitrix_client: BaseClient):
    """Test retrieving a user option and ensuring correctness."""

    bitrix_response = bitrix_client.user.option.get(
        option=_OPTION,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    option_value = bitrix_response.result

    assert option_value == _OPTION_VALUE, "User option value does not match"
