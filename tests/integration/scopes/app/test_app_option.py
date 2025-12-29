from typing import Text, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.app,
    pytest.mark.app_option,
]

_OPTION_NAME: Text = f"{Config().get_local_datetime().timestamp()}_test_option"
_OPTION_VALUE: Text = "test_option_value"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_option_set")
def test_option_set(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.app.option.set(
        options={
            _OPTION_NAME: _OPTION_VALUE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = cast(bool, bitrix_response.result)

    assert is_set is True, "Option set should return True"

    cache.set("option_name", _OPTION_NAME)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_option_get", depends=["test_option_set"])
def test_option_get(bitrix_client: Client, cache: Cache):
    """"""

    option_name = cache.get("option_name", None)
    assert isinstance(option_name, str), "Option name should be cached"

    bitrix_response = bitrix_client.app.option.get(
        option=option_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, (str, dict))

    option_value = cast(str, bitrix_response.result)

    assert option_value == _OPTION_VALUE, f"Option {option_name} value does not match"
