from typing import Iterable, Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_communication,
]

_FIELDS: Iterable[Text] = ("ID", "ACTIVITY_ID", "ENTITY_ID", "ENTITY_TYPE_ID", "TYPE", "VALUE")


def test_crm_activity_communication_fields(bitrix_client: BaseClient):
    """Test retrieving communication fields."""

    bitrix_response = bitrix_client.crm.activity.communication.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"
