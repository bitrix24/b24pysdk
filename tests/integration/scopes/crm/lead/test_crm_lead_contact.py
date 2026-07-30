from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIResponse, BitrixAPIValueResponse, BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit
from b24pysdk.schemas.crm.field import CRMField, CRMFieldsDict
from b24pysdk.schemas.crm.links import ContactLink

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_lead,
    pytest.mark.crm_lead_contact,
]

_FIELDS: Tuple[Text, ...] = ("CONTACT_ID", "SORT", "IS_PRIMARY")
_LEAD_TITLE: Text = f"{SDK_NAME} Lead Contact"
_CONTACT_NAME: Text = f"{SDK_NAME} Lead Contact"
_CONTACT_LAST_NAME: Text = "Lead"
_CONTACT_SORT: int = 100
_IS_PRIMARY: B24BoolLit = B24BoolLit.TRUE


@pytest.mark.dependency(name="test_crm_lead_contact_fields")
def test_crm_lead_contact_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.lead.contact.fields().response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    fields = bitrix_response.value

    assert isinstance(fields, CRMFieldsDict)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], CRMField), f"Field {field!r} should be CRMField"


@pytest.mark.dependency(name="test_crm_lead_contact_add", depends=["test_crm_lead_contact_fields"])
def test_crm_lead_contact_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_response = bitrix_client.crm.lead.add(
        fields={
            "TITLE": _LEAD_TITLE,
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
            "NAME": _CONTACT_NAME,
            "LAST_NAME": _CONTACT_LAST_NAME,
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

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    assert isinstance(bitrix_response.result, list)
    assert isinstance(bitrix_response.values, list)

    items = bitrix_response.values

    assert len(items) >= 1, "Expected at least one contact binding to be returned"

    for item in items:
        assert isinstance(item, ContactLink)
        if item.contact_id == contact_id:
            assert item.sort == _CONTACT_SORT
            assert item.is_primary is True
            break
    else:
        pytest.fail(f"Contact {contact_id} should be linked to lead {lead_id}")


@pytest.mark.dependency(name="test_crm_lead_contact_delete", depends=["test_crm_lead_contact_items_get"])
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


@pytest.mark.dependency(name="test_crm_lead_contact_items_delete", depends=["test_crm_lead_contact_delete"])
def test_crm_lead_contact_items_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_contact_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    contact_id = cache.get("lead_contact_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    add_response = bitrix_client.crm.lead.contact.add(
        bitrix_id=lead_id,
        fields={
            "CONTACT_ID": contact_id,
            "SORT": _CONTACT_SORT,
            "IS_PRIMARY": _IS_PRIMARY,
        },
    ).response

    assert isinstance(add_response, BitrixAPIResponse)
    assert isinstance(add_response.result, bool)
    assert add_response.result is True, "Lead contact binding should return True"

    bitrix_response = bitrix_client.crm.lead.contact.items.delete(
        bitrix_id=lead_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Lead contact items deletion should return True"


@pytest.mark.dependency(name="test_crm_lead_contact_cleanup", depends=["test_crm_lead_contact_items_delete"])
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
