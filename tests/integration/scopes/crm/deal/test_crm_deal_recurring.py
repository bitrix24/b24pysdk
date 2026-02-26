from datetime import timedelta
from typing import Generator, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal_recurring,
]

_FIELDS: Tuple[Text, ...] = ("ID", "DEAL_ID", "BASED_ID", "ACTIVE", "NEXT_EXECUTION", "LAST_EXECUTION", "COUNTER_REPEAT", "START_DATE", "CATEGORY_ID", "IS_LIMIT", "LIMIT_REPEAT", "LIMIT_DATE", "PARAMS")
_DEAL_ID: int = 27


@pytest.mark.dependency(name="test_recurring_fields")
def test_recurring_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.recurring.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_recurring_add", depends=["test_recurring_fields"])
def test_recurring_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    start_date = (Config().get_local_datetime() + timedelta(days=30)).isoformat()
    limit_date = (Config().get_local_datetime() + timedelta(days=365)).isoformat()


    bitrix_response = bitrix_client.crm.deal.recurring.add(
        fields={
            "DEAL_ID": _DEAL_ID,
            "CATEGORY_ID": "1",
            "IS_LIMIT": "D",
            "LIMIT_DATE": limit_date,
            "START_DATE": start_date,
            "PARAMS": {
                "MODE": "multiple",
                "MULTIPLE_TYPE": "month",
                "MULTIPLE_INTERVAL": 1,
                "OFFSET_BEGINDATE_TYPE": "day",
                "OFFSET_BEGINDATE_VALUE": 1,
                "OFFSET_CLOSEDATE_TYPE": "month",
                "OFFSET_CLOSEDATE_VALUE": 2,
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    recurring_id = bitrix_response.result

    assert recurring_id > 0, "Recurring deal creation should return a positive ID"

    cache.set("recurring_id", recurring_id)


@pytest.mark.dependency(name="test_recurring_get", depends=["test_recurring_add"])
def test_recurring_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    recurring_id = cache.get("recurring_id", None)
    assert isinstance(recurring_id, int), "Recurring ID should be cached"

    bitrix_response = bitrix_client.crm.deal.recurring.get(bitrix_id=recurring_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    recurring = bitrix_response.result

    assert recurring.get("ID") == str(recurring_id), "Recurring ID does not match"
    assert int(recurring.get("DEAL_ID", 0)) == _DEAL_ID, "Recurring DEAL_ID does not match"
    assert recurring.get("CATEGORY_ID") == "1", "Recurring CATEGORY_ID does not match"
    assert recurring.get("IS_LIMIT") == "D", "Recurring IS_LIMIT does not match"


@pytest.mark.dependency(name="test_recurring_update", depends=["test_recurring_add"])
def test_recurring_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    recurring_id = cache.get("recurring_id", None)
    assert isinstance(recurring_id, int), "Recurring ID should be cached"

    next_year = (Config().get_local_datetime() + timedelta(days=365)).isoformat()

    bitrix_response = bitrix_client.crm.deal.recurring.update(
        bitrix_id=recurring_id,
        fields={
            "CATEGORY_ID": "2",
            "START_DATE": next_year,
            "PARAMS": {
                "MODE": "single",
                "SINGLE_BEFORE_START_DATE_TYPE": "day",
                "SINGLE_BEFORE_START_DATE_VALUE": 5,
                "OFFSET_BEGINDATE_TYPE": "day",
                "OFFSET_BEGINDATE_VALUE": 1,
                "OFFSET_CLOSEDATE_TYPE": "month",
                "OFFSET_CLOSEDATE_VALUE": 2,
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_updated = bitrix_response.result
    assert is_updated is True, "Recurring deal update should return True"


@pytest.mark.dependency(name="test_recurring_list", depends=["test_recurring_update"])
def test_recurring_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    recurring_id = cache.get("recurring_id", None)
    assert isinstance(recurring_id, int), "Recurring ID should be cached"

    bitrix_response = bitrix_client.crm.deal.recurring.list(
        filter={"ID": recurring_id},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    recurring_list = bitrix_response.result

    assert len(recurring_list) == 1, "Expected one recurring deal to be returned"
    recurring = recurring_list[0]

    assert isinstance(recurring, dict)
    assert recurring.get("ID") == str(recurring_id), "Recurring ID does not match in list"
    assert int(recurring.get("DEAL_ID", 0)) == _DEAL_ID, "Recurring DEAL_ID does not match in list"
    assert recurring.get("CATEGORY_ID") == "2", "Recurring CATEGORY_ID does not match after update"


@pytest.mark.dependency(name="test_recurring_list_as_list", depends=["test_recurring_add"])
def test_recurring_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.recurring.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    recurring_list = bitrix_response.result

    assert len(recurring_list) >= 1, "Expected at least one recurring deal to be returned"

    for recurring in recurring_list:
        assert isinstance(recurring, dict)


@pytest.mark.dependency(name="test_recurring_list_as_list_fast", depends=["test_recurring_add"])
def test_recurring_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.recurring.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    recurring_list = bitrix_response.result

    last_recurring_id = None

    for recurring in recurring_list:
        assert isinstance(recurring, dict)
        assert "ID" in recurring

        recurring_id = int(recurring["ID"])

        if last_recurring_id is None:
            last_recurring_id = recurring_id
        else:
            assert last_recurring_id > recurring_id
            last_recurring_id = recurring_id


@pytest.mark.dependency(name="test_recurring_expose", depends=["test_recurring_update"])
def test_recurring_expose(bitrix_client: BaseClient, cache: Cache):
    """"""

    recurring_id = cache.get("recurring_id", None)
    assert isinstance(recurring_id, int), "Recurring ID should be cached"

    bitrix_response = bitrix_client.crm.deal.recurring.expose(bitrix_id=recurring_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    exposed_deal_id = bitrix_response.result

    assert exposed_deal_id > 0, "Exposed deal creation should return a positive ID"

    cache.set("exposed_deal_id", exposed_deal_id)


@pytest.mark.dependency(name="test_recurring_delete", depends=["test_recurring_expose"])
def test_recurring_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    recurring_id = cache.get("recurring_id", None)
    assert isinstance(recurring_id, int), "Recurring ID should be cached"

    bitrix_response = bitrix_client.crm.deal.recurring.delete(bitrix_id=recurring_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_deleted = bitrix_response.result
    assert is_deleted is True, "Recurring deal deletion should return True"
