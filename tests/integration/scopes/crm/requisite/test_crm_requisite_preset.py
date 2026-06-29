import pytest

from b24pysdk.api.responses import BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.requisite import RequisitePresetCountry

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_requisite,
    pytest.mark.crm_requisite_preset,
]


def test_countries(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.requisite.preset.countries().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    assert isinstance(bitrix_response.result, list)

    countries = bitrix_response.values

    assert countries, "Expected at least one requisite preset country to be returned"

    for country in countries:
        assert isinstance(country, RequisitePresetCountry)
        assert isinstance(country.bitrix_id, int)
        assert country.bitrix_id > 0
        assert isinstance(country.code, str)
        assert country.code
        assert isinstance(country.title, str)
        assert country.title
