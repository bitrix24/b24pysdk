from typing import Dict, Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.app,
]

_OAUTH_APP_FIELDS: Tuple[Text, ...] = ("ID", "CODE", "VERSION", "STATUS", "INSTALLED", "PAYMENT_EXPIRED", "DAYS", "LANGUAGE_ID", "LICENSE", "LICENSE_TYPE", "LICENSE_FAMILY")
_WEBHOOK_APP_FIELDS: Tuple[Text, ...] = ("SCOPE", "LICENSE")


def test_app_info(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.app.info().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    app_info = cast(Dict[Text, Text], bitrix_response.result)

    if "SCOPE" in app_info:
        for field in _WEBHOOK_APP_FIELDS:
            assert field in app_info, f"Field '{field}' should be present for webhook auth"
    else:
        for field in _OAUTH_APP_FIELDS:
            assert field in app_info, f"Field '{field}' should be present for OAuth"
