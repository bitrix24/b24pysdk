from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.pull,
    pytest.mark.pull_application_config,
]

_REQUIRED_FIELDS: Tuple[Text, ...] = ("server", "channels")


@pytest.mark.oauth_only
def test_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.pull.application.config.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "pull.application.config.get result should be a dict"

    config_data = bitrix_response.result

    for field in _REQUIRED_FIELDS:
        assert field in config_data, f"Field {field!r} should be present in pull.application.config.get result"
        assert isinstance(config_data[field], dict), f"Field {field!r} should be a dict"
