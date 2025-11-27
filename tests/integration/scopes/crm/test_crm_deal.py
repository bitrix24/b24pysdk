from typing import Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
]

_COMMON_FIELDS: Tuple[Text, ...] = ("ID", "TITLE")


def test_crm_deal_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.deal.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    assert isinstance(fields, dict), "CRM deal fields result should be a dictionary"

    for key in _COMMON_FIELDS:
        assert key in fields, f"Common field '{key}' should be present"
