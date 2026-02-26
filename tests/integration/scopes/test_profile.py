from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.profile,
]

_FIELDS: Tuple[Text, ...] = ("ID", "ADMIN", "NAME", "LAST_NAME", "PERSONAL_GENDER", "TIME_ZONE")


def test_profile(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.profile().response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    user_profile = bitrix_response.result

    assert isinstance(user_profile, dict), "User profile should be dict"

    for field in _FIELDS:
        assert field in user_profile, f"Field {field!r} should be present"
