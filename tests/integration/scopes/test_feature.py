from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.feature import FeatureGet

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.feature,
]

_CODE: Text = "rest_auth_connector"


def test_feature_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.feature.get(code=_CODE).response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    feature_get = bitrix_response.value

    assert isinstance(feature_get, FeatureGet), "Feature get value should be FeatureGet"
    assert feature_get.value is True, "FeatureGet.value should return True"
