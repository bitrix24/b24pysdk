import pytest

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.telephony,
    pytest.mark.telephony_call,
]

_TELEPHONY_TIMEOUT: int = 10
_REGISTER_FIELDS = ("CALL_ID",)
_FINISH_FIELDS = ("CALL_ID",)
_TRANSCRIPT_FIELDS = ("TRANSCRIPT_ID",)


@pytest.mark.oauth_only
def test_attach_transcription(bitrix_client: BaseClient):
    """"""

    phone_suffix = int(Config().get_local_datetime().timestamp() * (10 ** 6)) % 1000000000
    phone_number = f"+7999{phone_suffix:09d}"

    register_response = bitrix_client.telephony.external_call.register(
        phone_number=phone_number,
        call_type=2,
        user_id=BITRIX_PORTAL_OWNER_ID,
        crm_create=0,
        show=0,
        add_to_chat=0,
        external_call_id=f"{SDK_NAME}_TRANSCRIPT_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}",
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(register_response, BitrixAPIResponse)
    assert isinstance(register_response.result, dict), "telephony.externalCall.register result should be a dict"
    for field in _REGISTER_FIELDS:
        assert field in register_response.result, f"Field '{field}' should be present"

    call_id = register_response.result.get("CALL_ID")
    assert isinstance(call_id, str), "CALL_ID should be string"
    assert len(call_id) > 0, "CALL_ID should not be empty"

    finish_response = bitrix_client.telephony.external_call.finish(
        call_id=call_id,
        user_id=BITRIX_PORTAL_OWNER_ID,
        duration=2,
        status_code="200",
        add_to_chat=0,
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(finish_response, BitrixAPIResponse)
    assert isinstance(finish_response.result, dict), "telephony.externalCall.finish result should be a dict"
    for field in _FINISH_FIELDS:
        assert field in finish_response.result, f"Field '{field}' should be present"
    assert finish_response.result.get("CALL_ID") == call_id, "Finished CALL_ID should match registered CALL_ID"

    bitrix_response = bitrix_client.telephony.call.attach_transcription(
        call_id=call_id,
        messages=[
            {
                "SIDE": "User",
                "START_TIME": 0,
                "STOP_TIME": 1,
                "MESSAGE": f"{SDK_NAME} user replica",
            },
            {
                "SIDE": "Client",
                "START_TIME": 1,
                "STOP_TIME": 2,
                "MESSAGE": f"{SDK_NAME} client replica",
            },
        ],
        cost=1,
        cost_currency="USD",
        timeout=_TELEPHONY_TIMEOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "telephony.call.attachTranscription result should be a dict"
    for field in _TRANSCRIPT_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    transcript_data = bitrix_response.result
    transcript_id = transcript_data.get("TRANSCRIPT_ID")

    assert isinstance(transcript_id, int), "TRANSCRIPT_ID should be int"
    assert transcript_id > 0, "TRANSCRIPT_ID should be positive"
