import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPINotFound

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.vote,
    pytest.mark.vote_integration_im,
]

_SEND_RESULT_FIELDS = ("messageId", "voteId")


def test_send(bitrix_client: BaseClient):
    """"""

    chat_response = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT", message=f"{SDK_NAME} vote").response

    assert isinstance(chat_response, BitrixAPIResponse)
    assert isinstance(chat_response.result, int), "im.chat.add should return chat id"

    try:
        bitrix_response = bitrix_client.vote.integration.im.send(
            chat_id=chat_response.result,
            im_message_vote_data={
                "QUESTIONS": [
                    {
                        "QUESTION": f"{SDK_NAME} Question",
                        "FIELD_TYPE": 0,
                        "ANSWERS": [
                            {"MESSAGE": "Yes"},
                            {"MESSAGE": "No"},
                        ],
                    },
                ],
                "ANONYMITY": 0,
                "OPTIONS": 0,
            },
        ).response
    except BitrixAPINotFound:
        pytest.skip("vote.integration.im.send is not available on this portal")

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.integration.im.send result should be dict"

    send_data = bitrix_response.result
    for field in _SEND_RESULT_FIELDS:
        assert field in send_data, f"Field '{field}' should be present"
        assert isinstance(send_data[field], int), f"Field '{field}' should be int"
        assert send_data[field] > 0, f"Field '{field}' should be positive"
