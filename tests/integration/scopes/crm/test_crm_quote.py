from typing import Generator, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import (
    BitrixAPIListFastResponse,
    BitrixAPIListResponse,
    BitrixAPIResponse,
)
from b24pysdk.utils.types import JSONDictGenerator

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_quote,
]

_FIELDS: Tuple[Text, ...] = (
    "ID",
    "QUOTE_NUMBER",
    "TITLE",
    "STATUS_ID",
    "CURRENCY_ID",
    "OPPORTUNITY",
    "TAX_VALUE",
    "COMPANY_ID",
    "MYCOMPANY_ID",
    "CONTACT_IDS",
    "BEGINDATE",
    "CLOSEDATE",
    "OPENED",
    "CLOSED",
    "COMMENTS",
    "CONTENT",
    "TERMS",
    "ASSIGNED_BY_ID",
    "CREATED_BY_ID",
    "MODIFY_BY_ID",
    "DATE_CREATE",
    "DATE_MODIFY",
    "LEAD_ID",
    "DEAL_ID",
    "PERSON_TYPE_ID",
)

_TITLE: Text = f"{SDK_NAME} Test Quote"
_STATUS_ID: Text = "DRAFT"
_CURRENCY_ID: Text = "USD"
_OPPORTUNITY: float = 5000.0
_COMMENTS: Text = f"{SDK_NAME} test comment"
_BEGINDATE: Text = "2024-01-01T12:00:00"
_CLOSEDATE: Text = "2024-12-31T12:00:00"
_OPENED: Text = "Y"


@pytest.mark.dependency(name="test_quote_fields")
def test_quote_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.quote.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_quote_add", depends=["test_quote_fields"])
def test_quote_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.quote.add(
        fields={
            "TITLE": _TITLE,
            "STATUS_ID": _STATUS_ID,
            "CURRENCY_ID": _CURRENCY_ID,
            "OPPORTUNITY": _OPPORTUNITY,
            "COMMENTS": _COMMENTS,
            "BEGINDATE": _BEGINDATE,
            "CLOSEDATE": _CLOSEDATE,
            "OPENED": _OPENED,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    quote_id = cast(int, bitrix_response.result)

    assert quote_id > 0, "Quote creation should return a positive ID"

    cache.set("quote_id", quote_id)


@pytest.mark.dependency(name="test_quote_get", depends=["test_quote_add"])
def test_quote_get(bitrix_client: Client, cache: Cache):
    """"""

    quote_id = cache.get("quote_id", None)
    assert isinstance(quote_id, int), "Quote ID should be cached"

    bitrix_response = bitrix_client.crm.quote.get(bitrix_id=quote_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    quote = cast(dict, bitrix_response.result)

    assert quote.get("ID") == str(quote_id), "Quote ID does not match"
    assert quote.get("TITLE") == _TITLE, "Quote TITLE does not match"
    assert quote.get("STATUS_ID") == _STATUS_ID, "Quote STATUS_ID does not match"
    assert quote.get("CURRENCY_ID") == _CURRENCY_ID, "Quote CURRENCY_ID does not match"
    assert float(quote.get("OPPORTUNITY", 0)) == _OPPORTUNITY, "Quote OPPORTUNITY does not match"
    assert quote.get("COMMENTS") == _COMMENTS, "Quote COMMENTS does not match"
    assert quote.get("OPENED") == _OPENED, "Quote OPENED does not match"


@pytest.mark.dependency(name="test_quote_list", depends=["test_quote_add"])
def test_quote_list(bitrix_client: Client, cache: Cache):
    """"""

    quote_id = cache.get("quote_id", None)
    assert isinstance(quote_id, int), "Quote ID should be cached"

    bitrix_response = bitrix_client.crm.quote.list(
        filter={
            "ID": quote_id,
        },
        select=["ID", "TITLE", "STATUS_ID", "CURRENCY_ID", "OPPORTUNITY"],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    quotes = cast(list, bitrix_response.result)

    assert len(quotes) >= 1, "Expected at least one quote to be returned"

    for quote in quotes:
        assert isinstance(quote, dict)
        if all((
            quote.get("ID") == str(quote_id),
            quote.get("TITLE") == _TITLE,
            quote.get("STATUS_ID") == _STATUS_ID,
            quote.get("CURRENCY_ID") == _CURRENCY_ID,
            float(quote.get("OPPORTUNITY", 0)) == _OPPORTUNITY,
        )):
            break
    else:
        pytest.fail(f"Quote with ID {quote_id} should be found in list")


@pytest.mark.dependency(name="test_quote_list_as_list", depends=["test_quote_add"])
def test_quote_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.quote.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    quotes = cast(list, bitrix_response.result)

    assert len(quotes) >= 1, "Expected at least one quote to be returned"

    for quote in quotes:
        assert isinstance(quote, dict)


@pytest.mark.dependency(name="test_quote_list_as_list_fast", depends=["test_quote_add"])
def test_quote_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.quote.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    quotes = cast(JSONDictGenerator, bitrix_response.result)

    last_quote_id = None

    for quote in quotes:
        assert isinstance(quote, dict)
        assert "ID" in quote

        quote_id = int(quote["ID"])

        if last_quote_id is None:
            last_quote_id = quote_id
        else:
            assert last_quote_id > quote_id
            last_quote_id = quote_id


@pytest.mark.dependency(name="test_quote_update", depends=["test_quote_add"])
def test_quote_update(bitrix_client: Client, cache: Cache):
    """"""

    quote_id = cache.get("quote_id", None)
    assert isinstance(quote_id, int), "Quote ID should be cached"

    updated_comments = f"{_COMMENTS} - UPDATED"

    bitrix_response = bitrix_client.crm.quote.update(
        bitrix_id=quote_id,
        fields={
            "COMMENTS": updated_comments,
            "STATUS_ID": "SENT",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Quote update should return True"

    cache.set("updated_comments", updated_comments)


@pytest.mark.dependency(name="test_quote_delete", depends=["test_quote_update"])
def test_quote_delete(bitrix_client: Client, cache: Cache):
    """"""

    quote_id = cache.get("quote_id", None)
    assert isinstance(quote_id, int), "Quote ID should be cached"

    bitrix_response = bitrix_client.crm.quote.delete(bitrix_id=quote_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Quote deletion should return True"
