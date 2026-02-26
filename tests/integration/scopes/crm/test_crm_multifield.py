from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_multifield,
]

_FIELDS: Tuple[Text, ...] = ("ID", "TYPE_ID", "VALUE", "VALUE_TYPE")


def test_crm_multifield_fields(bitrix_client: BaseClient):
    """Test retrieving description of multiple fields."""

    bitrix_response = bitrix_client.crm.multifield.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"
