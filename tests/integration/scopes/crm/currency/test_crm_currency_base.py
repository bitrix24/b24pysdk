from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_currency_base,
]

_CURRENCY_CODE: Text = "USD"


@pytest.mark.dependency(name="test_currency_base_set")
def test_currency_base_set(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.currency.base.set(bitrix_id=_CURRENCY_CODE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = bitrix_response.result

    assert is_set is True, "Currency base set should return True"


@pytest.mark.dependency(name="test_currency_base_get", depends=["test_currency_base_set"])
def test_currency_base_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.currency.base.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str)

    base_currency = bitrix_response.result

    assert base_currency == _CURRENCY_CODE, f"Base currency should be {_CURRENCY_CODE}"
