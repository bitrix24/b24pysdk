from typing import Iterable, Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_communication,
]

_FIELDS: Iterable[Text] = ("ID", "ACTIVITY_ID", "ENTITY_ID", "ENTITY_TYPE_ID", "TYPE", "VALUE")


def test_crm_activity_communication_fields(bitrix_client: Client):
    """Test retrieving communication fields."""

    bitrix_response = bitrix_client.crm.activity.communication.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"
