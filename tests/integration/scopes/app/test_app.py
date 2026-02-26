from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.app,
]

_OAUTH_FIELDS: Tuple[Text, ...] = ("ID", "CODE", "VERSION", "STATUS", "INSTALLED", "PAYMENT_EXPIRED", "DAYS", "LANGUAGE_ID", "LICENSE", "LICENSE_TYPE", "LICENSE_FAMILY")
_WEBHOOK_FIELDS: Tuple[Text, ...] = ("SCOPE", "LICENSE")


def test_app_info(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.app.info().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    app_info = bitrix_response.result

    if "ID" in app_info:
        for field in _OAUTH_FIELDS:
            assert field in app_info, f"Field '{field}' should be present for OAuth"

    else:
        for field in _WEBHOOK_FIELDS:
            assert field in app_info, f"Field '{field}' should be present for webhook auth"
