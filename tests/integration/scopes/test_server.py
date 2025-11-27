from datetime import datetime
from typing import cast

import pytest

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.server,
]


def test_server_time(bitrix_client: Client):
    """"""

    start_dt = datetime.now(tz=Config().tzinfo)

    bitrix_response = bitrix_client.server.time().response

    end_dt = datetime.now(tz=Config().tzinfo)

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str), "Server time result should be a str"

    server_dt_str = cast(str, bitrix_response.result)

    try:
        server_dt = datetime.fromisoformat(server_dt_str)
    except ValueError as error:
        pytest.fail(f"Server time is not a valid ISO datetime: {bitrix_response.result} ({error})")

    assert isinstance(server_dt, datetime), "Server time result should be a datetime object"
    assert start_dt <= server_dt <= end_dt, "Server time result should be between start and end"
