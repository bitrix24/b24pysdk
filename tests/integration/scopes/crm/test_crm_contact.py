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
    pytest.mark.crm_contact,
]

_FIELDS: Iterable[Text] = ("ID", "NAME", "SECOND_NAME", "LAST_NAME", "TYPE_ID", "SOURCE_ID", "POST", "OPENED", "ASSIGNED_BY_ID")
_NAME: Text = f"{SDK_NAME} First Name"
_SECOND_NAME: Text = f"{SDK_NAME} Middle Name"
_LAST_NAME: Text = f"{SDK_NAME} Last Name"
_TYPE_ID: Text = "CLIENT"
_SOURCE_ID: Text = "WEB"
_POST: Text = f"{SDK_NAME} Position"
_OPENED: Text = "Y"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated First Name"


@pytest.mark.dependency(name="test_crm_contact_fields")
def test_crm_contact_fields(bitrix_client: Client):
    """Test retrieving contact fields."""

    bitrix_response = bitrix_client.crm.contact.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_contact_add", depends=["test_crm_contact_fields"])
def test_crm_contact_add(bitrix_client: Client, cache: Cache):
    """Test creating a new contact."""

    bitrix_response = bitrix_client.crm.contact.add(
        fields={
            "NAME": _NAME,
            "SECOND_NAME": _SECOND_NAME,
            "LAST_NAME": _LAST_NAME,
            "TYPE_ID": _TYPE_ID,
            "SOURCE_ID": _SOURCE_ID,
            "POST": _POST,
            "OPENED": _OPENED,
        },
        params={
            "REGISTER_SONET_EVENT": "Y",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    contact_id = cast(int, bitrix_response.result)

    assert contact_id > 0, "Contact creation should return a positive ID"

    cache.set("contact_id", contact_id)


@pytest.mark.dependency(name="test_crm_contact_get", depends=["test_crm_contact_add"])
def test_crm_contact_get(bitrix_client: Client, cache: Cache):
    """Test retrieving a contact by ID."""

    contact_id = cache.get("contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached after addition"

    bitrix_response = bitrix_client.crm.contact.get(bitrix_id=contact_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    contact = cast(dict, bitrix_response.result)

    assert contact.get("ID") == str(contact_id), f"Contact ID does not match. Expected: {contact_id}, Got: {contact.get('ID')}"
    assert contact.get("NAME") == _NAME, "Contact first name does not match"
    assert contact.get("SECOND_NAME") == _SECOND_NAME, "Contact middle name does not match"
    assert contact.get("LAST_NAME") == _LAST_NAME, "Contact last name does not match"
    assert contact.get("TYPE_ID") == _TYPE_ID, "Contact type ID does not match"
    assert contact.get("SOURCE_ID") == _SOURCE_ID, "Contact source ID does not match"
    assert contact.get("POST") == _POST, "Contact position does not match"
    assert contact.get("OPENED") == _OPENED, "Contact opened status does not match"


@pytest.mark.dependency(name="test_crm_contact_list", depends=["test_crm_contact_get"])
def test_crm_contact_list(bitrix_client: Client, cache: Cache):
    """Test retrieving a list of contacts."""

    contact_id = cache.get("contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.contact.list(
        select=list(_FIELDS),
        filter={"ID": contact_id},
        order={"ID": "desc"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    contacts = cast(list, bitrix_response.result)

    for contact in contacts:
        assert isinstance(contact, dict)
        if all((
            contact.get("ID") == str(contact_id),
            contact.get("NAME") == _NAME,
            contact.get("SECOND_NAME") == _SECOND_NAME,
            contact.get("LAST_NAME") == _LAST_NAME,
            contact.get("TYPE_ID") == _TYPE_ID,
            contact.get("SOURCE_ID") == _SOURCE_ID,
            contact.get("POST") == _POST,
            contact.get("OPENED") == _OPENED,
        )):
            break
    else:
        pytest.fail(f"Test contact with ID {contact_id} should be found in list")


@pytest.mark.dependency(name="test_crm_contact_list_as_list", depends=["test_crm_contact_list"])
def test_crm_contact_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.contact.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    contacts = cast(list, bitrix_response.result)

    assert len(contacts) >= 1, "Expected at least one contact to be returned"

    for contact in contacts:
        assert isinstance(contact, dict)


@pytest.mark.dependency(name="test_crm_contact_list_as_list_fast", depends=["test_crm_contact_list_as_list"])
def test_crm_contact_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.contact.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    contacts = cast(JSONDictGenerator, bitrix_response.result)

    last_contact_id = None

    for contact in contacts:
        assert isinstance(contact, dict)
        assert "ID" in contact

        contact_id = int(contact["ID"])

        if last_contact_id is None:
            last_contact_id = contact_id
        else:
            assert last_contact_id > contact_id
            last_contact_id = contact_id


@pytest.mark.dependency(name="test_crm_contact_update", depends=["test_crm_contact_list_as_list_fast"])
def test_crm_contact_update(bitrix_client: Client, cache: Cache):
    """Test updating an existing contact."""

    contact_id = cache.get("contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.contact.update(
        bitrix_id=contact_id,
        fields={
            "NAME": _UPDATED_NAME,
        },
        params={
            "REGISTER_SONET_EVENT": "Y",
            "REGISTER_HISTORY_EVENT": "Y",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Contact update should return True"


@pytest.mark.dependency(name="test_crm_contact_delete", depends=["test_crm_contact_update"])
def test_crm_contact_delete(bitrix_client: Client, cache: Cache):
    """Test deleting a contact."""

    contact_id = cache.get("contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    bitrix_response = bitrix_client.crm.contact.delete(bitrix_id=contact_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Contact deletion should return True"
