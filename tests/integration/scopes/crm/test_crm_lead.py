from typing import Generator, Iterable, Text, cast

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
    pytest.mark.crm_lead,
]

_FIELDS: Iterable[Text] = ("ID", "TITLE", "NAME", "LAST_NAME", "STATUS_ID", "ASSIGNED_BY_ID", "CURRENCY_ID", "OPPORTUNITY")
_TITLE: Text = f"{SDK_NAME} Lead Title"
_NAME: Text = f"{SDK_NAME} First Name"
_LAST_NAME: Text = f"{SDK_NAME} Last Name"
_STATUS_ID: Text = "CONVERTED"
_CURRENCY_ID: Text = "USD"
_OPPORTUNITY: Text = "12500.00"
_UPDATED_TITLE: Text = f"{SDK_NAME} Updated Lead Title"


@pytest.mark.dependency(name="test_crm_lead_fields")
def test_crm_lead_fields(bitrix_client: Client):
    """Test retrieving lead fields."""

    bitrix_response = bitrix_client.crm.lead.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_lead_add", depends=["test_crm_lead_fields"])
def test_crm_lead_add(bitrix_client: Client, cache: Cache):
    """Test creating a new lead."""

    bitrix_response = bitrix_client.crm.lead.add(
        fields={
            "TITLE": _TITLE,
            "NAME": _NAME,
            "LAST_NAME": _LAST_NAME,
            "STATUS_ID": _STATUS_ID,
            "CURRENCY_ID": _CURRENCY_ID,
            "OPPORTUNITY": _OPPORTUNITY,
        },
        params={
            "REGISTER_SONET_EVENT": "Y",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    lead_id = cast(int, bitrix_response.result)

    assert lead_id > 0, "Lead creation should return a positive ID"

    cache.set("lead_id", lead_id)


@pytest.mark.dependency(name="test_crm_lead_get", depends=["test_crm_lead_add"])
def test_crm_lead_get(bitrix_client: Client, cache: Cache):
    """Test retrieving a lead by ID."""

    lead_id = cache.get("lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached after addition"

    bitrix_response = bitrix_client.crm.lead.get(bitrix_id=lead_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    lead = cast(dict, bitrix_response.result)

    assert lead.get("ID") == str(lead_id), "Lead ID does not match"
    assert lead.get("TITLE") == _TITLE, "Lead title does not match"
    assert lead.get("NAME") == _NAME, "Lead first name does not match"
    assert lead.get("LAST_NAME") == _LAST_NAME, "Lead last name does not match"
    assert lead.get("STATUS_ID") == _STATUS_ID, "Lead status ID does not match"
    assert lead.get("CURRENCY_ID") == _CURRENCY_ID, "Lead currency ID does not match"
    assert lead.get("OPPORTUNITY") == _OPPORTUNITY, "Lead opportunity does not match"


@pytest.mark.dependency(name="test_crm_lead_list", depends=["test_crm_lead_get"])
def test_crm_lead_list(bitrix_client: Client, cache: Cache):
    """Test retrieving a list of leads."""

    lead_id = cache.get("lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    bitrix_response = bitrix_client.crm.lead.list(
        select=list(_FIELDS),
        filter={"=STATUS_ID": _STATUS_ID},
        order={"ID": "desc"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    leads = cast(list, bitrix_response.result)

    assert len(leads) >= 1, "Expected at least one lead to be returned"

    for lead in leads:
        assert isinstance(lead, dict)
        if all((
                lead.get("ID") == str(lead_id),
                lead.get("TITLE") == _TITLE,
                lead.get("NAME") == _NAME,
                lead.get("LAST_NAME") == _LAST_NAME,
        )):
            break
    else:
        pytest.fail(f"Test lead with ID {lead_id} should be found in list")


@pytest.mark.dependency(name="test_crm_lead_list_as_list", depends=["test_crm_lead_list"])
def test_crm_lead_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.lead.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    leads = cast(list, bitrix_response.result)

    assert len(leads) >= 1, "Expected at least one lead to be returned"

    for lead in leads:
        assert isinstance(lead, dict)


@pytest.mark.dependency(name="test_crm_lead_list_as_list_fast", depends=["test_crm_lead_list_as_list"])
def test_crm_lead_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.lead.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    leads = cast(JSONDictGenerator, bitrix_response.result)

    last_lead_id = None

    for lead in leads:
        assert isinstance(lead, dict)
        assert "ID" in lead

        lead_id = int(lead["ID"])

        if last_lead_id is None:
            last_lead_id = lead_id
        else:
            assert last_lead_id > lead_id
            last_lead_id = lead_id


@pytest.mark.dependency(name="test_crm_lead_update", depends=["test_crm_lead_list_as_list_fast"])
def test_crm_lead_update(bitrix_client: Client, cache: Cache):
    """Test updating an existing lead."""

    lead_id = cache.get("lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    bitrix_response = bitrix_client.crm.lead.update(
        bitrix_id=lead_id,
        fields={
            "TITLE": _UPDATED_TITLE,
        },
        params={
            "REGISTER_SONET_EVENT": "Y",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Lead update should return True"


@pytest.mark.dependency(name="test_crm_lead_delete", depends=["test_crm_lead_update"])
def test_crm_lead_delete(bitrix_client: Client, cache: Cache):
    """Test deleting a lead."""

    lead_id = cache.get("lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    bitrix_response = bitrix_client.crm.lead.delete(bitrix_id=lead_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Lead deletion should return True"
