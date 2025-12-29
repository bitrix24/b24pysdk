from typing import Generator, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.utils.types import JSONDictGenerator
from tests.constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
]

_FIELDS: Tuple[Text, ...] = (
"ID", "TITLE", "TYPE_ID", "CATEGORY_ID", "STAGE_ID", "STAGE_SEMANTIC_ID", "IS_NEW", "IS_RECURRING",
"IS_RETURN_CUSTOMER", "IS_REPEATED_APPROACH", "PROBABILITY", "CURRENCY_ID", "OPPORTUNITY", "IS_MANUAL_OPPORTUNITY",
"TAX_VALUE", "COMPANY_ID", "CONTACT_ID", "CONTACT_IDS", "QUOTE_ID", "BEGINDATE", "CLOSEDATE", "OPENED", "CLOSED",
"COMMENTS", "ASSIGNED_BY_ID", "CREATED_BY_ID", "MODIFY_BY_ID", "MOVED_BY_ID", "DATE_CREATE", "DATE_MODIFY",
"MOVED_TIME", "SOURCE_ID", "SOURCE_DESCRIPTION", "LEAD_ID", "ADDITIONAL_INFO", "LOCATION_ID", "ORIGINATOR_ID",
"ORIGIN_ID", "UTM_SOURCE", "UTM_MEDIUM", "UTM_CAMPAIGN", "UTM_CONTENT", "UTM_TERM", "LAST_ACTIVITY_TIME",
"LAST_ACTIVITY_BY")

_TITLE: Text = f"{SDK_NAME} Deal"
_TYPE_ID: Text = "GOODS"
_STAGE_ID: Text = "NEW"
_CURRENCY_ID: Text = "USD"
_OPPORTUNITY: float = 1000.00
_COMMENTS: Text = f"{SDK_NAME} Test Deal Comment"
_UPDATED_TITLE: Text = f"{SDK_NAME} Updated Deal"
_UPDATED_OPPORTUNITY: float = 2000.00


@pytest.mark.dependency(name="test_deal_fields")
def test_deal_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.deal.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_deal_add", depends=["test_deal_fields"])
def test_deal_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.deal.add(
        fields={
            "TITLE": _TITLE,
            "TYPE_ID": _TYPE_ID,
            "STAGE_ID": _STAGE_ID,
            "CURRENCY_ID": _CURRENCY_ID,
            "OPPORTUNITY": _OPPORTUNITY,
            "COMMENTS": _COMMENTS,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    deal_id = cast(int, bitrix_response.result)

    assert deal_id > 0, "Deal creation should return a positive ID"

    cache.set("deal_id", deal_id)


@pytest.mark.dependency(name="test_deal_get", depends=["test_deal_add"])
def test_deal_get(bitrix_client: Client, cache: Cache):
    """"""

    deal_id = cache.get("deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    bitrix_response = bitrix_client.crm.deal.get(bitrix_id=deal_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    deal = cast(dict, bitrix_response.result)

    assert deal.get("ID") == str(deal_id), "Deal ID does not match"
    assert deal.get("TITLE") == _TITLE, "Deal TITLE does not match"
    assert deal.get("TYPE_ID") == _TYPE_ID, "Deal TYPE_ID does not match"
    assert deal.get("STAGE_ID") == _STAGE_ID, "Deal STAGE_ID does not match"
    assert deal.get("CURRENCY_ID") == _CURRENCY_ID, "Deal CURRENCY_ID does not match"
    assert float(deal.get("OPPORTUNITY", 0)) == _OPPORTUNITY, "Deal OPPORTUNITY does not match"
    assert deal.get("COMMENTS") == _COMMENTS, "Deal COMMENTS does not match"


@pytest.mark.dependency(name="test_deal_update", depends=["test_deal_get"])
def test_deal_update(bitrix_client: Client, cache: Cache):
    """"""

    deal_id = cache.get("deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    bitrix_response = bitrix_client.crm.deal.update(
        bitrix_id=deal_id,
        fields={
            "TITLE": _UPDATED_TITLE,
            "OPPORTUNITY": _UPDATED_OPPORTUNITY,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_updated = cast(bool, bitrix_response.result)
    assert is_updated is True, "Deal update should return True"


@pytest.mark.dependency(name="test_deal_list", depends=["test_deal_update"])
def test_deal_list(bitrix_client: Client, cache: Cache):
    """"""

    deal_id = cache.get("deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    bitrix_response = bitrix_client.crm.deal.list(
        filter={"ID": deal_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    deals = cast(list, bitrix_response.result)

    assert len(deals) == 1, "Expected one deal to be returned"
    deal = deals[0]

    assert isinstance(deal, dict)
    assert deal.get("ID") == str(deal_id), "Deal ID does not match in list"
    assert deal.get("TITLE") == _UPDATED_TITLE, "Deal TITLE does not match after update"
    assert float(deal.get("OPPORTUNITY", 0)) == _UPDATED_OPPORTUNITY, "Deal OPPORTUNITY does not match after update"


@pytest.mark.dependency(name="test_deal_list_as_list", depends=["test_deal_list"])
def test_deal_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.deal.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    deals = cast(list, bitrix_response.result)

    assert len(deals) >= 1, "Expected at least one deal to be returned"

    for deal in deals:
        assert isinstance(deal, dict)


@pytest.mark.dependency(name="test_deal_list_as_list_fast", depends=["test_deal_list_as_list"])
def test_deal_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.deal.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    deals = cast(JSONDictGenerator, bitrix_response.result)

    last_deal_id = None

    for deal in deals:
        assert isinstance(deal, dict)
        assert "ID" in deal

        deal_id = int(deal["ID"])

        if last_deal_id is None:
            last_deal_id = deal_id
        else:
            assert last_deal_id > deal_id
            last_deal_id = deal_id


@pytest.mark.dependency(name="test_deal_delete", depends=["test_deal_list_as_list_fast"])
def test_deal_delete(bitrix_client: Client, cache: Cache):
    """"""

    deal_id = cache.get("deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    bitrix_response = bitrix_client.crm.deal.delete(bitrix_id=deal_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_deleted = cast(bool, bitrix_response.result)
    assert is_deleted is True, "Deal deletion should return True"
