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
    pytest.mark.crm_lead,
    pytest.mark.crm_lead_contact,
]

_FIELDS: Tuple[Text, ...] = ("CONTACT_ID", "SORT", "IS_PRIMARY")
_CONTACT_SORT: int = 100
_IS_PRIMARY: B24BoolLit = B24BoolLit.TRUE


@pytest.mark.dependency(name="test_crm_lead_contact_fields")
def test_crm_lead_contact_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.lead.contact.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_crm_lead_contact_add", depends=["test_crm_lead_contact_fields"])
def test_crm_lead_contact_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    lead_title: Text = f"{SDK_NAME} Lead Contact {timestamp}"
    contact_name: Text = f"{SDK_NAME} Lead Contact"
    contact_last_name: Text = f"{timestamp}"

    lead_response = bitrix_client.crm.lead.add(
        fields={
            "TITLE": lead_title,
            "STATUS_ID": "NEW",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 1,
        },
    ).response

    assert isinstance(lead_response, BitrixAPIResponse)
    assert isinstance(lead_response.result, int)

    lead_id = lead_response.result
    assert lead_id > 0, "Lead creation should return a positive ID"

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

    bitrix_response = bitrix_client.crm.lead.contact.add(
        bitrix_id=lead_id,
        fields={
            "CONTACT_ID": contact_id,
            "SORT": _CONTACT_SORT,
            "IS_PRIMARY": _IS_PRIMARY,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_added = bitrix_response.result
    assert is_added is True, "Lead contact binding should return True"

    cache.set("lead_contact_lead_id", lead_id)
    cache.set("lead_contact_contact_id", contact_id)


@pytest.mark.dependency(name="test_crm_lead_contact_items_get", depends=["test_crm_lead_contact_add"])
def test_crm_lead_contact_items_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_contact_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    contact_id = cache.get("lead_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.lead.contact.items.get(
        bitrix_id=lead_id,
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
        pytest.fail(f"Contact {contact_id} should be linked to lead {lead_id}")


@pytest.mark.dependency(name="test_crm_lead_contact_delete", depends=["test_crm_lead_contact_add"])
def test_crm_lead_contact_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_contact_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    contact_id = cache.get("lead_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.lead.contact.delete(
        bitrix_id=lead_id,
        fields={
            "CONTACT_ID": contact_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Lead contact binding deletion should return True"


@pytest.mark.dependency(name="test_crm_lead_contact_cleanup", depends=["test_crm_lead_contact_delete"])
def test_crm_lead_contact_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_contact_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    contact_id = cache.get("lead_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    lead_delete = bitrix_client.crm.lead.delete(bitrix_id=lead_id).response
    assert isinstance(lead_delete, BitrixAPIResponse)
    assert isinstance(lead_delete.result, bool)
    assert lead_delete.result is True, "Lead deletion should return True"

    contact_delete = bitrix_client.crm.contact.delete(bitrix_id=contact_id).response
    assert isinstance(contact_delete, BitrixAPIResponse)
    assert isinstance(contact_delete.result, bool)
    assert contact_delete.result is True, "Contact deletion should return True"
