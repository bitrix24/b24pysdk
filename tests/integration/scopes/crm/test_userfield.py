import pytest

from b24pysdk.api.responses import BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.userfield import CRMUserfieldType

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_userfield,
]


def test_types(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.userfield.types().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    assert isinstance(bitrix_response.result, list)

    userfield_types = bitrix_response.values

    assert userfield_types, "Expected at least one user field type to be returned"

    for userfield_type in userfield_types:
        assert isinstance(userfield_type, CRMUserfieldType)
        assert isinstance(userfield_type.bitrix_id, str)
        assert userfield_type.bitrix_id
        assert isinstance(userfield_type.title, str)
        assert userfield_type.title
