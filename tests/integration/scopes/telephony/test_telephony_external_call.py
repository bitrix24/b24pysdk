from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.telephony,
    pytest.mark.telephony_external_call,
]

_PHONE_NUMBER_PREFIX: Text = "+7999"
_TELEPHONY_TIMEOUT: int = 10
_REGISTER_FIELDS = ("CALL_ID",)
_SEARCH_FIELDS = ("CRM_ENTITY_TYPE", "CRM_ENTITY_ID", "ASSIGNED_BY_ID", "NAME", "ASSIGNED_BY")
_FINISH_FIELDS = ("CALL_ID",)
_ATTACH_RECORD_FIELDS = ("uploadUrl", "fieldName")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_register")
def test_register(bitrix_client: BaseClient, cache: Cache):
    """"""

    phone_suffix = int(Config().get_local_datetime().timestamp() * (10 ** 6)) % 1000000000
    phone_number = f"{_PHONE_NUMBER_PREFIX}{phone_suffix:09d}"

    bitrix_response = bitrix_client.telephony.external_call.register(
        phone_number=phone_number,
        call_type=2,
        user_id=BITRIX_PORTAL_OWNER_ID,
        crm_create=0,
        show=0,
        add_to_chat=0,
        external_call_id=f"{SDK_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "telephony.externalCall.register result should be a dict"
    for field in _REGISTER_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    register_data = bitrix_response.result
    call_id = register_data.get("CALL_ID")
    assert isinstance(call_id, str), "CALL_ID should be a string"
    assert len(call_id) > 0, "CALL_ID should not be empty"

    cache.set("telephony_external_call_id", call_id)
    cache.set("telephony_external_call_phone_number", phone_number)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_search_crm_entities", depends=["test_telephony_external_call_register"])
def test_search_crm_entities(bitrix_client: BaseClient, cache: Cache):
    """"""

    phone_number = cache.get("telephony_external_call_phone_number", None)
    assert isinstance(phone_number, str), "Phone number should be cached"

    bitrix_response = bitrix_client.telephony.external_call.search_crm_entities(
        phone_number=phone_number,
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "telephony.externalCall.searchCrmEntities result should be a list"

    crm_entities = bitrix_response.result

    for crm_entity in crm_entities:
        assert isinstance(crm_entity, dict), "Each CRM entity should be a dict"
        for field in _SEARCH_FIELDS:
            assert field in crm_entity, f"Field '{field}' should be present"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_show", depends=["test_telephony_external_call_register"])
def test_show(bitrix_client: BaseClient, cache: Cache):
    """"""

    call_id = cache.get("telephony_external_call_id", None)
    assert isinstance(call_id, str), "CALL_ID should be cached"

    bitrix_response = bitrix_client.telephony.external_call.show(
        call_id=call_id,
        user_id=BITRIX_PORTAL_OWNER_ID,
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "telephony.externalCall.show result should be bool"
    assert bitrix_response.result is True, "telephony.externalCall.show should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_hide", depends=["test_telephony_external_call_show"])
def test_hide(bitrix_client: BaseClient, cache: Cache):
    """"""

    call_id = cache.get("telephony_external_call_id", None)
    assert isinstance(call_id, str), "CALL_ID should be cached"

    bitrix_response = bitrix_client.telephony.external_call.hide(
        call_id=call_id,
        user_id=BITRIX_PORTAL_OWNER_ID,
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "telephony.externalCall.hide result should be bool"
    assert bitrix_response.result is True, "telephony.externalCall.hide should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_finish", depends=["test_telephony_external_call_hide"])
def test_finish(bitrix_client: BaseClient, cache: Cache):
    """"""

    call_id = cache.get("telephony_external_call_id", None)
    assert isinstance(call_id, str), "CALL_ID should be cached"

    bitrix_response = bitrix_client.telephony.external_call.finish(
        call_id=call_id,
        user_id=BITRIX_PORTAL_OWNER_ID,
        duration=1,
        status_code="200",
        add_to_chat=0,
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "telephony.externalCall.finish result should be a dict"
    for field in _FINISH_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    finish_data = bitrix_response.result
    assert finish_data.get("CALL_ID") == call_id, "CALL_ID in finish response should match registered call"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_call_attach_record", depends=["test_telephony_external_call_finish"])
def test_attach_record(bitrix_client: BaseClient, cache: Cache):
    """"""

    call_id = cache.get("telephony_external_call_id", None)
    assert isinstance(call_id, str), "CALL_ID should be cached"

    bitrix_response = bitrix_client.telephony.external_call.attach_record(
        call_id=call_id,
        filename=f"{SDK_NAME.lower()}-record.mp3",
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "telephony.externalCall.attachRecord result should be a dict"
    for field in _ATTACH_RECORD_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    record_data = bitrix_response.result
    assert isinstance(record_data.get("uploadUrl"), str), "uploadUrl should be a string"
    assert len(record_data["uploadUrl"]) > 0, "uploadUrl should not be empty"
    assert isinstance(record_data.get("fieldName"), str), "fieldName should be a string"
    assert len(record_data["fieldName"]) > 0, "fieldName should not be empty"
