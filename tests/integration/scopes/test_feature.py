from typing import Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from b24pysdk.constants import B24BoolLit

pytestmark = [
    pytest.mark.integration,
    pytest.mark.feature,
]

_CODE: Text = "rest_auth_connector"
_RESULT_FIELD: Text = "value"
_RESULT_VALUE: B24BoolLit = B24BoolLit.TRUE


def test_feature_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.feature.get(code=_CODE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    feature_data = cast(dict, bitrix_response.result)

    assert _RESULT_FIELD in feature_data, f"Field {_RESULT_FIELD!r} should be present"
    assert feature_data[_RESULT_FIELD] == _RESULT_VALUE, f"Value should be {_RESULT_VALUE!r}"
