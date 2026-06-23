from datetime import datetime

import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.server,
]


def test_server_time(bitrix_client: BaseClient):
    """"""

    start_dt = Config().get_local_datetime()

    bitrix_response = bitrix_client.server.time().response

    end_dt = Config().get_local_datetime()

    assert isinstance(bitrix_response, BitrixAPIValueResponse)
    assert isinstance(bitrix_response.result, str), "Server time result should be a str"

    server_time = bitrix_response.value

    assert isinstance(server_time, datetime), "Server time result should be a datetime object"
    assert start_dt.replace(microsecond=0) <= server_time <= end_dt.replace(microsecond=0), "Server time result should be between start and end"
