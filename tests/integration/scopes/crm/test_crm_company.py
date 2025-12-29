from typing import Generator, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.utils.types import JSONDictGenerator

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_company,
]

_FIELDS: Tuple[Text, ...] = ("ID", "TITLE", "COMPANY_TYPE", "INDUSTRY", "EMPLOYEES", "CURRENCY_ID", "REVENUE", "OPENED", "ASSIGNED_BY_ID", "PHONE", "EMAIL", "DATE_CREATE", "DATE_MODIFY", "CREATED_BY_ID", "MODIFY_BY_ID", "ADDRESS", "ADDRESS_CITY", "ADDRESS_COUNTRY", "ADDRESS_POSTAL_CODE", "BANKING_DETAILS", "COMMENTS", "HAS_EMAIL", "HAS_PHONE", "IM", "IS_MY_COMPANY", "LEAD_ID", "LOGO", "ORIGINATOR_ID", "ORIGIN_ID", "ORIGIN_VERSION", "REG_ADDRESS", "UTM_SOURCE", "UTM_MEDIUM", "UTM_CAMPAIGN", "UTM_CONTENT", "UTM_TERM", "WEB")

_TITLE: Text = f"{SDK_NAME} Company"
_COMPANY_TYPE: Text = "CUSTOMER"
_INDUSTRY: Text = "MANUFACTURING"
_EMPLOYEES: Text = "EMPLOYEES_2"
_CURRENCY_ID: Text = "USD"
_REVENUE: float = 3000000.00
_UPDATED_REVENUE: float = 500000.00
_UPDATED_EMPLOYEES: Text = "EMPLOYEES_3"


def test_company_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.company.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_company_add")
def test_company_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.company.add(
        fields={
            "TITLE": _TITLE,
            "COMPANY_TYPE": _COMPANY_TYPE,
            "INDUSTRY": _INDUSTRY,
            "EMPLOYEES": _EMPLOYEES,
            "CURRENCY_ID": _CURRENCY_ID,
            "REVENUE": _REVENUE,
            "OPENED": "Y",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    company_id = cast(int, bitrix_response.result)

    assert company_id > 0, "Company creation should return a positive ID"

    cache.set("company_id", company_id)


@pytest.mark.dependency(name="test_company_get", depends=["test_company_add"])
def test_company_get(bitrix_client: Client, cache: Cache):
    """"""

    company_id = cache.get("company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.company.get(bitrix_id=company_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    company = cast(dict, bitrix_response.result)

    assert company.get("ID") == str(company_id), "Company ID does not match"
    assert company.get("TITLE") == _TITLE, "Company TITLE does not match"
    assert company.get("COMPANY_TYPE") == _COMPANY_TYPE, "Company COMPANY_TYPE does not match"
    assert company.get("INDUSTRY") == _INDUSTRY, "Company INDUSTRY does not match"
    assert company.get("EMPLOYEES") == _EMPLOYEES, "Company EMPLOYEES does not match"
    assert company.get("CURRENCY_ID") == _CURRENCY_ID, "Company CURRENCY_ID does not match"
    assert float(company.get("REVENUE", 0)) == _REVENUE, "Company REVENUE does not match"


@pytest.mark.dependency(name="test_company_update", depends=["test_company_add"])
def test_company_update(bitrix_client: Client, cache: Cache):
    """"""

    company_id = cache.get("company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.company.update(
        bitrix_id=company_id,
        fields={
            "REVENUE": _UPDATED_REVENUE,
            "EMPLOYEES": _UPDATED_EMPLOYEES,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Company update should return True"


@pytest.mark.dependency(name="test_company_list", depends=["test_company_update"])
def test_company_list(bitrix_client: Client, cache: Cache):
    """"""

    company_id = cache.get("company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.company.list(
        filter={"ID": company_id},
        select=["ID", "TITLE", "CURRENCY_ID", "REVENUE", "EMPLOYEES"],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    companies = cast(list, bitrix_response.result)

    assert len(companies) == 1, "Expected one company to be returned"
    company = companies[0]

    assert isinstance(company, dict)
    assert company.get("ID") == str(company_id), "Company ID does not match in list"
    assert company.get("TITLE") == _TITLE, "Company TITLE does not match in list"
    assert float(company.get("REVENUE", 0)) == _UPDATED_REVENUE, "Company REVENUE does not match after update"
    assert company.get("EMPLOYEES") == _UPDATED_EMPLOYEES, "Company EMPLOYEES does not match after update"


@pytest.mark.dependency(name="test_company_list_as_list", depends=["test_company_add"])
def test_company_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.company.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    companies = cast(list, bitrix_response.result)

    assert len(companies) >= 1, "Expected at least one company to be returned"

    for company in companies:
        assert isinstance(company, dict)


@pytest.mark.dependency(name="test_company_list_as_list_fast", depends=["test_company_add"])
def test_company_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.company.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    companies = cast(JSONDictGenerator, bitrix_response.result)

    last_company_id = None

    for company in companies:
        assert isinstance(company, dict)
        assert "ID" in company

        company_id = int(company["ID"])

        if last_company_id is None:
            last_company_id = company_id
        else:
            assert last_company_id > company_id
            last_company_id = company_id


@pytest.mark.dependency(name="test_company_delete", depends=["test_company_list"])
def test_company_delete(bitrix_client: Client, cache: Cache):
    """"""

    company_id = cache.get("company_id", None)
    assert isinstance(company_id, int), "Company ID should be cached"

    bitrix_response = bitrix_client.crm.company.delete(bitrix_id=company_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_deleted = cast(bool, bitrix_response.result)
    assert is_deleted is True, "Company deletion should return True"
