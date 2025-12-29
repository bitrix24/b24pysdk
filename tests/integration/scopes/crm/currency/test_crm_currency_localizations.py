from typing import Text, Tuple, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from b24pysdk.utils.types import JSONDict

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_currency_localizations,
]

_FIELDS: Tuple[Text, ...] = ("FULL_NAME", "FORMAT_STRING", "DEC_POINT", "THOUSANDS_VARIANT", "THOUSANDS_SEP", "DECIMALS", "HIDE_ZERO")

_CURRENCY_ID: Text = "USD"
_LANG_EN: Text = "en"

_LOCALIZATIONS_EN: JSONDict = {
    "FULL_NAME": "United States Dollar",
    "FORMAT_STRING": "$#",
    "DEC_POINT": ".",
    "THOUSANDS_VARIANT": "C",
    "THOUSANDS_SEP": ",",
    "DECIMALS": "2",
    "HIDE_ZERO": "Y",
}


@pytest.mark.dependency(name="test_localizations_fields")
def test_localizations_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.localizations.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_localizations_set", depends=["test_localizations_fields"])
def test_localizations_set(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.localizations.set(
        bitrix_id=_CURRENCY_ID,
        localizations={
            _LANG_EN: _LOCALIZATIONS_EN,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_set = cast(bool, bitrix_response.result)

    assert is_set is True, "Setting localizations should return True"


@pytest.mark.dependency(name="test_localizations_get", depends=["test_localizations_set"])
def test_localizations_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.localizations.get(
        bitrix_id=_CURRENCY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    localizations = cast(dict, bitrix_response.result)

    assert localizations.get(_LANG_EN) == _LOCALIZATIONS_EN, f"Localization {_LANG_EN} should be in result"


@pytest.mark.dependency(name="test_localizations_delete", depends=["test_localizations_get"])
def test_localizations_delete(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.localizations.delete(
        bitrix_id=_CURRENCY_ID,
        lids=[_LANG_EN],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Deleting localizations should return True"
