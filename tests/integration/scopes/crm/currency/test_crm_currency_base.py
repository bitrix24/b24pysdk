from typing import Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_currency_base,
]

_CURRENCY_CODE: Text = "USD"


@pytest.mark.dependency(name="test_currency_base_set")
def test_currency_base_set(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.base.set(bitrix_id=_CURRENCY_CODE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = cast(bool, bitrix_response.result)

    assert is_set is True, "Currency base set should return True"


@pytest.mark.dependency(name="test_currency_base_get", depends=["test_currency_base_set"])
def test_currency_base_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.base.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str)

    base_currency = cast(str, bitrix_response.result)

    assert base_currency == _CURRENCY_CODE, f"Base currency should be {_CURRENCY_CODE}"
