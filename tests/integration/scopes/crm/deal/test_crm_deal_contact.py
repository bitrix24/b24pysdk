from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
    pytest.mark.crm_deal_contact,
]

_FIELDS: Tuple[Text, ...] = ("CONTACT_ID", "SORT", "IS_PRIMARY")
_CONTACT_SORT: int = 100
_IS_PRIMARY: B24BoolLit = B24BoolLit.TRUE


@pytest.mark.dependency(name="test_crm_deal_contact_fields")
def test_crm_deal_contact_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.contact.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_crm_deal_contact_add", depends=["test_crm_deal_contact_fields"])
def test_crm_deal_contact_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    deal_title: Text = f"{SDK_NAME} Deal Contact {timestamp}"
    contact_name: Text = f"{SDK_NAME} Deal Contact"
    contact_last_name: Text = f"{timestamp}"

    deal_response = bitrix_client.crm.deal.add(
        fields={
            "TITLE": deal_title,
            "STAGE_ID": "NEW",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 1,
        },
    ).response

    assert isinstance(deal_response, BitrixAPIResponse)
    assert isinstance(deal_response.result, int)

    deal_id = deal_response.result
    assert deal_id > 0, "Deal creation should return a positive ID"

    contact_response = bitrix_client.crm.contact.add(
        fields={
            "NAME": contact_name,
            "LAST_NAME": contact_last_name,
        },
    ).response

    assert isinstance(contact_response, BitrixAPIResponse)
    assert isinstance(contact_response.result, int)

    contact_id = contact_response.result
    assert contact_id > 0, "Contact creation should return a positive ID"

    bitrix_response = bitrix_client.crm.deal.contact.add(
        bitrix_id=deal_id,
        fields={
            "CONTACT_ID": contact_id,
            "SORT": _CONTACT_SORT,
            "IS_PRIMARY": _IS_PRIMARY,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_added = bitrix_response.result
    assert is_added is True, "Deal contact binding should return True"

    cache.set("deal_contact_deal_id", deal_id)
    cache.set("deal_contact_contact_id", contact_id)


@pytest.mark.dependency(name="test_crm_deal_contact_items_get", depends=["test_crm_deal_contact_add"])
def test_crm_deal_contact_items_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    deal_id = cache.get("deal_contact_deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    contact_id = cache.get("deal_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.deal.contact.items.get(
        bitrix_id=deal_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    items = bitrix_response.result

    assert len(items) >= 1, "Expected at least one contact binding to be returned"

    for item in items:
        assert isinstance(item, dict)
        if item.get("CONTACT_ID") in (contact_id, str(contact_id)):
            break
    else:
        pytest.fail(f"Contact {contact_id} should be linked to deal {deal_id}")


@pytest.mark.dependency(name="test_crm_deal_contact_delete", depends=["test_crm_deal_contact_add"])
def test_crm_deal_contact_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    deal_id = cache.get("deal_contact_deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    contact_id = cache.get("deal_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.deal.contact.delete(
        bitrix_id=deal_id,
        fields={
            "CONTACT_ID": contact_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Deal contact binding deletion should return True"


@pytest.mark.dependency(name="test_crm_deal_contact_cleanup", depends=["test_crm_deal_contact_delete"])
def test_crm_deal_contact_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    deal_id = cache.get("deal_contact_deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    contact_id = cache.get("deal_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    deal_delete = bitrix_client.crm.deal.delete(bitrix_id=deal_id).response
    assert isinstance(deal_delete, BitrixAPIResponse)
    assert isinstance(deal_delete.result, bool)
    assert deal_delete.result is True, "Deal deletion should return True"

    contact_delete = bitrix_client.crm.contact.delete(bitrix_id=contact_id).response
    assert isinstance(contact_delete, BitrixAPIResponse)
    assert isinstance(contact_delete.result, bool)
    assert contact_delete.result is True, "Contact deletion should return True"
