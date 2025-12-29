from typing import Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_currency,
]

_FIELDS: Tuple[Text, ...] = ("CURRENCY", "AMOUNT_CNT", "AMOUNT", "BASE", "SORT", "DATE_UPDATE", "LID", "FORMAT_STRING", "FULL_NAME", "DEC_POINT", "THOUSANDS_SEP", "DECIMALS", "LANG")

_CURRENCY_ID: Text = "TST"
_AMOUNT_CNT: int = 1
_AMOUNT: float = 1.2345
_SORT: int = 999
_UPDATED_AMOUNT: float = 2.3456
_UPDATED_SORT: int = 998


def test_currency_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.currency.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_currency_add")
def test_currency_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.currency.add(
        fields={
            "CURRENCY": _CURRENCY_ID,
            "AMOUNT_CNT": _AMOUNT_CNT,
            "AMOUNT": _AMOUNT,
            "SORT": _SORT,
            "BASE": "N",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, str)

    currency_id = cast(str, bitrix_response.result)

    assert currency_id == _CURRENCY_ID, "Currency creation should return currency ID"

    cache.set("currency_id", currency_id)


@pytest.mark.dependency(name="test_currency_get", depends=["test_currency_add"])
def test_currency_get(bitrix_client: Client, cache: Cache):
    """"""

    currency_id = cache.get("currency_id", None)
    assert isinstance(currency_id, str), "Currency ID should be cached"

    bitrix_response = bitrix_client.crm.currency.get(bitrix_id=currency_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    currency = cast(dict, bitrix_response.result)

    assert currency.get("CURRENCY") == _CURRENCY_ID, "Currency CURRENCY does not match"
    assert int(currency.get("AMOUNT_CNT", 0)) == _AMOUNT_CNT, "Currency AMOUNT_CNT does not match"
    assert float(currency.get("AMOUNT", 0)) == _AMOUNT, "Currency AMOUNT does not match"
    assert int(currency.get("SORT", 0)) == _SORT, "Currency SORT does not match"
    assert currency.get("BASE") == "N", "Currency BASE does not match"


@pytest.mark.dependency(name="test_currency_update", depends=["test_currency_add"])
def test_currency_update(bitrix_client: Client, cache: Cache):
    """"""

    currency_id = cache.get("currency_id", None)
    assert isinstance(currency_id, str), "Currency ID should be cached"

    bitrix_response = bitrix_client.crm.currency.update(
        bitrix_id=currency_id,
        fields={
            "AMOUNT": _UPDATED_AMOUNT,
            "SORT": _UPDATED_SORT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_updated = cast(bool, bitrix_response.result)
    assert is_updated is True, "Currency update should return True"


@pytest.mark.dependency(name="test_currency_list", depends=["test_currency_update"])
def test_currency_list(bitrix_client: Client, cache: Cache):
    """"""

    currency_id = cache.get("currency_id", None)
    assert isinstance(currency_id, str), "Currency ID should be cached"

    bitrix_response = bitrix_client.crm.currency.list(
        order={"SORT": "asc"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    currencies = cast(list, bitrix_response.result)

    for currency in currencies:
        assert isinstance(currency, dict)
        if all((currency.get("CURRENCY") == _CURRENCY_ID,
               float(currency.get("AMOUNT", 0)) == _UPDATED_AMOUNT,
               int(currency.get("SORT", 0)) == _UPDATED_SORT)):
            break
    else:
        pytest.fail(f"Test currency {_CURRENCY_ID} should be found in list")


@pytest.mark.dependency(name="test_currency_delete", depends=["test_currency_list"])
def test_currency_delete(bitrix_client: Client, cache: Cache):
    """"""

    currency_id = cache.get("currency_id", None)
    assert isinstance(currency_id, str), "Currency ID should be cached"

    bitrix_response = bitrix_client.crm.currency.delete(bitrix_id=currency_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_deleted = cast(bool, bitrix_response.result)
    assert is_deleted is True, "Currency deletion should return True"
