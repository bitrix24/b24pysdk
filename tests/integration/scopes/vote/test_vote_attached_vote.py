from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixResponseJSONDecodeError

from ....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.vote,
    pytest.mark.vote_attached_vote,
]

_ATTACH_FIELDS: Tuple[Text, ...] = ("ID", "VOTE_ID", "QUESTIONS")
_IM_ENTITY_TYPE: Text = "Bitrix\\Vote\\Attachment\\ImMessageConnector"


def _extract_answer_id_from_attach(attach: dict) -> int:
    question = next(iter(attach.get("QUESTIONS", {}).values()), None)
    if question is None:
        pytest.skip("No questions available for attached vote")

    answer = next(iter(question.get("ANSWERS", {}).values()), None)
    if answer is None:
        pytest.skip("No answers available for attached vote")

    answer_id = answer.get("ID")

    if isinstance(answer_id, str) and answer_id.isdigit():
        answer_id = int(answer_id)

    if not isinstance(answer_id, int):
        pytest.skip("No valid answer_id available for attached vote")

    return answer_id


@pytest.mark.dependency(name="test_vote_attached_vote_prepare")
def test_prepare(bitrix_client: BaseClient, cache: Cache):
    """"""

    chat_response = bitrix_client.im.chat.add(
        users=[BITRIX_PORTAL_OWNER_ID],
        type="CHAT",
        message=f"{SDK_NAME} vote",
    ).response
    chat_id = chat_response.result
    assert isinstance(chat_id, int), "im.chat.add should return chat id"

    send_response = bitrix_client.vote.integration.im.send(
        chat_id=chat_id,
        im_message_vote_data={
            "QUESTIONS": [
                {
                    "QUESTION": f"{SDK_NAME} Question",
                    "FIELD_TYPE": 0,
                    "ANSWERS": [{"MESSAGE": "Yes"}, {"MESSAGE": "No"}],
                },
            ],
            "ANONYMITY": 0,
            "OPTIONS": 0,
        },
    ).response
    assert isinstance(send_response, BitrixAPIResponse)
    assert isinstance(send_response.result, dict), "vote.integration.im.send result should be dict"

    attach_id = send_response.result.get("voteId")
    if isinstance(attach_id, str) and attach_id.isdigit():
        attach_id = int(attach_id)
    assert isinstance(attach_id, int), "voteId should be int"

    get_response = bitrix_client.vote.attached_vote.get(attach_id=attach_id).response
    assert isinstance(get_response, BitrixAPIResponse)
    assert isinstance(get_response.result, dict), "vote.attached_vote.get result should be dict"

    attach = get_response.result.get("attach")
    assert isinstance(attach, dict), "vote.attached_vote.get should contain attach dict"

    entity_id = attach.get("entityId")
    if isinstance(entity_id, str) and entity_id.isdigit():
        entity_id = int(entity_id)
    assert isinstance(entity_id, int), "attach.entityId should be int"

    assert attach_id > 0, "attach_id should be positive"
    assert entity_id > 0, "attach.entityId should be positive"

    cache.set("vote_attach_id", attach_id)
    cache.set("vote_entity_id", entity_id)


@pytest.mark.dependency(name="test_vote_attached_vote_get", depends=["test_vote_attached_vote_prepare"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    bitrix_response = bitrix_client.vote.attached_vote.get(attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.attached_vote.get result should be a dict"

    attach = bitrix_response.result.get("attach")
    assert isinstance(attach, dict), "vote.attached_vote.get result should contain attach dict"

    for field in _ATTACH_FIELDS:
        assert field in attach, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_vote_attached_vote_download", depends=["test_vote_attached_vote_prepare"])
def test_download(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    with pytest.raises(BitrixResponseJSONDecodeError):
        _ = bitrix_client.vote.attached_vote.download(attach_id=attach_id).response


@pytest.mark.dependency(name="test_vote_attached_vote_get_with_voted", depends=["test_vote_attached_vote_prepare"])
def test_get_with_voted(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    bitrix_response = bitrix_client.vote.attached_vote.get_with_voted(attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.attached_vote.get_with_voted result should be a dict"
    assert isinstance(bitrix_response.result.get("attach"), dict), "vote.attached_vote.get_with_voted should contain attach dict"


@pytest.mark.dependency(name="test_vote_attached_vote_get_many", depends=["test_vote_attached_vote_prepare"])
def test_get_many(bitrix_client: BaseClient, cache: Cache):
    """"""

    entity_id = cache.get("vote_entity_id", None)
    assert isinstance(entity_id, int), "entity_id should be cached"

    bitrix_response = bitrix_client.vote.attached_vote.get_many(
        module_id="im",
        entity_type=_IM_ENTITY_TYPE,
        entity_ids=[entity_id],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.attached_vote.get_many result should be a dict"
    items = bitrix_response.result.get("items", [])
    assert isinstance(items, list), "vote.attached_vote.get_many should return items list"
    assert len(items) > 0, "vote.attached_vote.get_many should return non-empty items list"
    created_item = next((item for item in items if item.get("entityId") == entity_id), None)
    assert isinstance(created_item, dict), "Created entity should be present in vote.attached_vote.get_many result"

    for field in _ATTACH_FIELDS:
        assert field in created_item, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_vote_attached_vote_get_answer_voted", depends=["test_vote_attached_vote_get"])
def test_get_answer_voted(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    vote_response = bitrix_client.vote.attached_vote.get(attach_id=attach_id).response

    assert isinstance(vote_response, BitrixAPIResponse)
    assert isinstance(vote_response.result, dict), "vote.attached_vote.get result should be a dict"

    attach = vote_response.result.get("attach")
    assert isinstance(attach, dict), "vote.attached_vote.get result should contain attach dict"

    answer_id = _extract_answer_id_from_attach(attach)

    bitrix_response = bitrix_client.vote.attached_vote.get_answer_voted(answer_id=answer_id, attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.attached_vote.get_answer_voted result should be a dict"


@pytest.mark.dependency(name="test_vote_attached_vote_vote", depends=["test_vote_attached_vote_get"])
def test_vote(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    vote_response = bitrix_client.vote.attached_vote.get(attach_id=attach_id).response

    assert isinstance(vote_response, BitrixAPIResponse)
    assert isinstance(vote_response.result, dict), "vote.attached_vote.get result should be a dict"

    attach = vote_response.result.get("attach")
    assert isinstance(attach, dict), "vote.attached_vote.get result should contain attach dict"

    answer_id = _extract_answer_id_from_attach(attach)

    bitrix_response = bitrix_client.vote.attached_vote.vote(
        ballot={"answers": [answer_id]},
        attach_id=attach_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result == [], "vote.attached_vote.vote should return empty list"


@pytest.mark.dependency(name="test_vote_attached_vote_recall", depends=["test_vote_attached_vote_vote"])
def test_recall(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    bitrix_response = bitrix_client.vote.attached_vote.recall(attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "vote.attached_vote.recall result should be dict"
    assert isinstance(bitrix_response.result.get("attach"), dict), "vote.attached_vote.recall should contain attach dict"


@pytest.mark.dependency(name="test_vote_attached_vote_resume", depends=["test_vote_attached_vote_prepare"])
def test_resume(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    stop_response = bitrix_client.vote.attached_vote.stop(attach_id=attach_id).response
    assert isinstance(stop_response, BitrixAPIResponse)
    assert stop_response.result == [], "vote.attached_vote.stop should return empty list"

    bitrix_response = bitrix_client.vote.attached_vote.resume(attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result == [], "vote.attached_vote.resume should return empty list"


@pytest.mark.dependency(name="test_vote_attached_vote_stop", depends=["test_vote_attached_vote_prepare"])
def test_stop(bitrix_client: BaseClient, cache: Cache):
    """"""

    attach_id = cache.get("vote_attach_id", None)
    assert isinstance(attach_id, int), "attach_id should be cached"

    bitrix_response = bitrix_client.vote.attached_vote.stop(attach_id=attach_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert bitrix_response.result == [], "vote.attached_vote.stop should return empty list"
