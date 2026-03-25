from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.timeman,
]

_REQUIRED_STATUS_FIELD: Text = "STATUS"


def test_status(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.status().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "Timeman status result should be a dict"

    status_data = bitrix_response.result
    assert len(status_data) > 0, "Timeman status result should not be empty"

    assert _REQUIRED_STATUS_FIELD in status_data, f"Field {_REQUIRED_STATUS_FIELD!r} should be present in timeman.status"
    assert isinstance(status_data[_REQUIRED_STATUS_FIELD], str), "Timeman STATUS should be a string"


def test_settings(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.timeman.settings().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "Timeman settings result should be a dict"

    settings_data = bitrix_response.result
    assert len(settings_data) > 0, "Timeman settings result should not be empty"

    for field, value in settings_data.items():
        assert isinstance(field, str), "timeman.settings field names should be strings"
        assert isinstance(value, (int, str, bool, list, dict)), "timeman.settings field value has unexpected type"


def test_open(bitrix_client: BaseClient):
    """"""

    current_status_response = bitrix_client.timeman.status().response

    assert isinstance(current_status_response, BitrixAPIResponse)
    assert isinstance(current_status_response.result, dict)

    current_status = current_status_response.result.get("STATUS")
    assert isinstance(current_status, str)

    if current_status not in ("CLOSED", "EXPIRED"):
        pytest.skip("timeman.open requires CLOSED or EXPIRED status")

    bitrix_response = bitrix_client.timeman.open().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "timeman.open result should be a dict"

    opened_status = bitrix_response.result.get("STATUS")
    assert opened_status == "OPENED", "timeman.open should return OPENED status"


def test_pause(bitrix_client: BaseClient):
    """"""

    current_status_response = bitrix_client.timeman.status().response

    assert isinstance(current_status_response, BitrixAPIResponse)
    assert isinstance(current_status_response.result, dict)

    current_status = current_status_response.result.get("STATUS")
    assert isinstance(current_status, str)

    if current_status != "OPENED":
        pytest.skip("timeman.pause requires OPENED status")

    bitrix_response = bitrix_client.timeman.pause().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "timeman.pause result should be a dict"

    paused_status = bitrix_response.result.get("STATUS")
    assert paused_status == "PAUSED", "timeman.pause should return PAUSED status"


def test_close(bitrix_client: BaseClient):
    """"""

    current_status_response = bitrix_client.timeman.status().response

    assert isinstance(current_status_response, BitrixAPIResponse)
    assert isinstance(current_status_response.result, dict)

    current_status = current_status_response.result.get("STATUS")
    assert isinstance(current_status, str)

    if current_status not in ("OPENED", "PAUSED"):
        pytest.skip("timeman.close requires OPENED or PAUSED status")

    bitrix_response = bitrix_client.timeman.close().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "timeman.close result should be a dict"

    closed_status = bitrix_response.result.get("STATUS")
    assert closed_status == "CLOSED", "timeman.close should return CLOSED status"
