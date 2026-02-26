from typing import Generator, Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit
from b24pysdk.constants.userfield import UserTypeID
from b24pysdk.utils.types import JSONDict

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
    pytest.mark.crm_deal_userfield,
]

_USER_TYPE_ID: UserTypeID = UserTypeID.STRING
_MULTIPLE: B24BoolLit = B24BoolLit.FALSE
_XML_ID: Text = "DEAL_UF_XML_ID"
_SORT: Text = "100"
_MANDATORY: B24BoolLit = B24BoolLit.FALSE
_SHOW_FILTER: B24BoolLit = B24BoolLit.TRUE
_SHOW_IN_LIST: B24BoolLit = B24BoolLit.TRUE
_EDIT_IN_LIST: B24BoolLit = B24BoolLit.TRUE
_SETTINGS_DEFAULT_VALUE: Text = f"{SDK_NAME} DEAL UF DEFAULT"
_SETTINGS_ROWS: int = 3
_SETTINGS: JSONDict = {
    "DEFAULT_VALUE": _SETTINGS_DEFAULT_VALUE,
    "ROWS": _SETTINGS_ROWS,
}


@pytest.mark.dependency(name="test_crm_deal_userfield_add")
def test_crm_deal_userfield_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfield_name = f"UF_CRM_{SDK_NAME.upper()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.crm.deal.userfield.add(
        fields={
            "FIELD_NAME": userfield_name,
            "USER_TYPE_ID": _USER_TYPE_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    userfield_id = bitrix_response.result
    assert userfield_id > 0, "Userfield creation should return a positive ID"

    cache.set("deal_userfield_id", userfield_id)
    cache.set("deal_userfield_name", userfield_name)


@pytest.mark.dependency(name="test_crm_deal_userfield_update", depends=["test_crm_deal_userfield_add"])
def test_crm_deal_userfield_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfield_id = cache.get("deal_userfield_id", None)
    assert isinstance(userfield_id, int), "Userfield ID should be cached"

    bitrix_response = bitrix_client.crm.deal.userfield.update(
        bitrix_id=userfield_id,
        fields={
            "XML_ID": _XML_ID,
            "SORT": _SORT,
            "MULTIPLE": _MULTIPLE,
            "MANDATORY": _MANDATORY,
            "SHOW_FILTER": _SHOW_FILTER,
            "SHOW_IN_LIST": _SHOW_IN_LIST,
            "EDIT_IN_LIST": _EDIT_IN_LIST,
            "SETTINGS": _SETTINGS,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_updated = bitrix_response.result
    assert is_updated is True, "Userfield update should return True"


@pytest.mark.dependency(name="test_crm_deal_userfield_list", depends=["test_crm_deal_userfield_update"])
def test_crm_deal_userfield_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfield_id = cache.get("deal_userfield_id", None)
    assert isinstance(userfield_id, int), "Userfield ID should be cached"

    userfield_name = cache.get("deal_userfield_name", None)
    assert isinstance(userfield_name, str), "Userfield name should be cached"

    bitrix_response = bitrix_client.crm.deal.userfield.list(
        filter={
            "ID": userfield_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    userfields = bitrix_response.result

    assert len(userfields) == 1, "Expected one userfield to be returned"

    userfield = userfields[0]

    assert isinstance(userfield, dict)
    assert userfield.get("ID") == str(userfield_id), "Userfield ID does not match"
    assert userfield.get("FIELD_NAME") == userfield_name, "Userfield FIELD_NAME does not match"
    assert userfield.get("USER_TYPE_ID") == _USER_TYPE_ID, "Userfield USER_TYPE_ID does not match"
    assert userfield.get("XML_ID") == _XML_ID, "Userfield XML_ID does not match"
    assert userfield.get("SORT") == _SORT, "Userfield SORT does not match"
    assert userfield.get("SHOW_IN_LIST") == _SHOW_IN_LIST, "Userfield SHOW_IN_LIST does not match"
    assert userfield.get("EDIT_IN_LIST") == _EDIT_IN_LIST, "Userfield EDIT_IN_LIST does not match"

    assert isinstance(userfield.get("SETTINGS"), dict), "Userfield SETTINGS is not a dictionary"

    userfield_settings = userfield["SETTINGS"]
    assert userfield_settings.get("DEFAULT_VALUE") == _SETTINGS_DEFAULT_VALUE, "Userfield SETTINGS DEFAULT_VALUE does not match"
    assert userfield_settings.get("ROWS") == _SETTINGS_ROWS, "Userfield SETTINGS ROWS does not match"


@pytest.mark.dependency(name="test_crm_deal_userfield_list_as_list", depends=["test_crm_deal_userfield_update"])
def test_crm_deal_userfield_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.userfield.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    userfields = bitrix_response.result

    assert len(userfields) >= 1, "Expected at least one userfield to be returned"

    for userfield in userfields:
        assert isinstance(userfield, dict)


@pytest.mark.dependency(name="test_crm_deal_userfield_list_as_list_fast", depends=["test_crm_deal_userfield_update"])
def test_crm_deal_userfield_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.deal.userfield.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    userfields = bitrix_response.result

    last_userfield_id = None

    for userfield in userfields:
        assert isinstance(userfield, dict)
        assert "ID" in userfield

        userfield_id = int(userfield["ID"])

        if last_userfield_id is None:
            last_userfield_id = userfield_id
        else:
            assert last_userfield_id > userfield_id
            last_userfield_id = userfield_id


@pytest.mark.dependency(name="test_crm_deal_userfield_delete", depends=["test_crm_deal_userfield_list_as_list_fast"])
def test_crm_deal_userfield_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    userfield_id = cache.get("deal_userfield_id", None)
    assert isinstance(userfield_id, int), "Userfield ID should be cached"

    bitrix_response = bitrix_client.crm.deal.userfield.delete(
        bitrix_id=userfield_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Userfield deletion should return True"
