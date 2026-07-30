from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIResponse, BitrixAPIValueResponse, BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit
from b24pysdk.schemas.crm.field import CRMField, CRMFieldsDict
from b24pysdk.schemas.crm.links import CompanyLink

from .....constants import SDK_NAME, SORT

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_contact,
    pytest.mark.crm_contact_company,
]

_FIELDS: Tuple[Text, ...] = ("COMPANY_ID", "SORT", "IS_PRIMARY")
_CONTACT_NAME: Text = f"{SDK_NAME} Contact Company"
_CONTACT_LAST_NAME: Text = "Contact"
_COMPANY_TITLE: Text = f"{SDK_NAME} Contact Company"
_SORT: int = SORT
_IS_PRIMARY: B24BoolLit = B24BoolLit.TRUE


@pytest.mark.dependency(name="test_crm_contact_company_fields")
def test_crm_contact_company_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.contact.company.fields().response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    fields = bitrix_response.value

    assert isinstance(fields, CRMFieldsDict)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], CRMField), f"Field {field!r} should be CRMField"


@pytest.mark.dependency(name="test_crm_contact_company_add")
def test_crm_contact_company_add(bitrix_client: BaseClient, cache: Cache):
    """"""

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

    company_response = bitrix_client.crm.company.add(
        fields={
            "TITLE": _COMPANY_TITLE,
        },
    ).response

    assert isinstance(company_response, BitrixAPIResponse)
    assert isinstance(company_response.result, int)

    company_id = company_response.result
    assert company_id > 0, "Company creation should return a positive ID"

    bitrix_response = bitrix_client.crm.contact.company.add(
        bitrix_id=contact_id,
        fields={
            "COMPANY_ID": company_id,
            "SORT": _SORT,
            "IS_PRIMARY": _IS_PRIMARY,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_added = bitrix_response.result
    assert is_added is True, "Contact company binding should return True"

    cache.set("contact_company_contact_id", contact_id)
    cache.set("contact_company_company_id", company_id)


@pytest.mark.dependency(name="test_crm_contact_company_items_get", depends=["test_crm_contact_company_add"])
def test_crm_contact_company_items_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    contact_id = cache.get("contact_company_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    company_id = cache.get("contact_company_company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.contact.company.items.get(
        bitrix_id=contact_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    assert isinstance(bitrix_response.result, list)
    assert isinstance(bitrix_response.values, list)

    items = bitrix_response.values

    assert len(items) >= 1, "Expected at least one company binding to be returned"

    for item in items:
        assert isinstance(item, CompanyLink)
        if item.company_id == company_id:
            assert item.sort == _SORT
            assert item.is_primary is True
            break
    else:
        pytest.fail(f"Company {company_id} should be linked to contact {contact_id}")


@pytest.mark.dependency(name="test_crm_contact_company_delete", depends=["test_crm_contact_company_items_get"])
def test_crm_contact_company_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    contact_id = cache.get("contact_company_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    company_id = cache.get("contact_company_company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.contact.company.delete(
        bitrix_id=contact_id,
        fields={
            "COMPANY_ID": company_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Contact company binding deletion should return True"


@pytest.mark.dependency(name="test_crm_contact_company_items_delete", depends=["test_crm_contact_company_delete"])
def test_crm_contact_company_items_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    contact_id = cache.get("contact_company_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    company_id = cache.get("contact_company_company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    add_response = bitrix_client.crm.contact.company.add(
        bitrix_id=contact_id,
        fields={
            "COMPANY_ID": company_id,
            "SORT": _SORT,
            "IS_PRIMARY": _IS_PRIMARY,
        },
    ).response

    assert isinstance(add_response, BitrixAPIResponse)
    assert isinstance(add_response.result, bool)
    assert add_response.result is True, "Contact company binding should return True"

    bitrix_response = bitrix_client.crm.contact.company.items.delete(
        bitrix_id=contact_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Contact company items deletion should return True"


@pytest.mark.dependency(name="test_crm_contact_company_cleanup", depends=["test_crm_contact_company_items_delete"])
def test_crm_contact_company_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    contact_id = cache.get("contact_company_contact_id", None)
    assert isinstance(contact_id, int), "Contact ID should be cached"

    company_id = cache.get("contact_company_company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    contact_delete = bitrix_client.crm.contact.delete(bitrix_id=contact_id).response
    assert isinstance(contact_delete, BitrixAPIResponse)
    assert isinstance(contact_delete.result, bool)
    assert contact_delete.result is True, "Contact deletion should return True"

    company_delete = bitrix_client.crm.company.delete(bitrix_id=company_id).response
    assert isinstance(company_delete, BitrixAPIResponse)
    assert isinstance(company_delete.result, bool)
    assert company_delete.result is True, "Company deletion should return True"
