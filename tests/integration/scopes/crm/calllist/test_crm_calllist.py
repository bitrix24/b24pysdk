from typing import Generator, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_calllist,
]

_ENTITY_TYPE: Text = "CONTACT"
_ENTITY_TYPE_ID: int = 3
_ENTITIES: Tuple[int] = (1,)
_UPDATED_ENTITIES: Tuple[int, ...] = (1, 3)
_STATUS_LIST_FIELDS: Tuple = ("ID", "NAME", "SORT", "STATUS_ID")


def test_calllist_statuslist(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.calllist.statuslist().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    statuses = bitrix_response.result

    assert len(statuses) >= 1, "Expected at least one call status to be returned"

    for status in statuses:
        assert isinstance(status, dict)
        for field in _STATUS_LIST_FIELDS:
            assert field in status, f"Field {field} should be present"


@pytest.mark.dependency(name="test_calllist_add")
def test_calllist_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.calllist.add(
        entity_type=_ENTITY_TYPE,
        entities=_ENTITIES,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    calllist_id = bitrix_response.result

    assert calllist_id > 0, "Call list creation should return a positive ID"

    cache.set("calllist_id", calllist_id)


@pytest.mark.dependency(name="test_calllist_get", depends=["test_calllist_add"])
def test_calllist_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    calllist_id = cache.get("calllist_id", None)
    assert isinstance(calllist_id, int), "Call list ID should be cached"

    bitrix_response = bitrix_client.crm.calllist.get(bitrix_id=calllist_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    calllist = bitrix_response.result

    assert calllist.get("ID") == str(calllist_id), "Call list ID does not match"
    assert calllist.get("ENTITY_TYPE") == _ENTITY_TYPE, "Call list ENTITY_TYPE does not match"


@pytest.mark.dependency(name="test_calllist_update", depends=["test_calllist_add"])
def test_calllist_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    calllist_id = cache.get("calllist_id", None)
    assert isinstance(calllist_id, int), "Call list ID should be cached"

    bitrix_response = bitrix_client.crm.calllist.update(
        list_id=calllist_id,
        entity_type=_ENTITY_TYPE,
        entities=_UPDATED_ENTITIES,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result

    assert is_updated is True, "Call list update should return True"


@pytest.mark.dependency(name="test_calllist_list", depends=["test_calllist_update"])
def test_calllist_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    calllist_id = cache.get("calllist_id", None)
    assert isinstance(calllist_id, int), "Call list ID should be cached"

    bitrix_response = bitrix_client.crm.calllist.list(
        filter={"ID": calllist_id},
        select=["ID", "CREATED_BY_ID", "ENTITY_TYPE_ID", "WEBFORM_ID"],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    calllists = bitrix_response.result

    assert len(calllists) == 1, "Expected one call list to be returned"

    calllist = calllists[0]

    assert isinstance(calllist, dict)
    assert calllist.get("ID") == str(calllist_id), "Call list ID does not match in list"
    assert calllist.get("ENTITY_TYPE_ID") == str(_ENTITY_TYPE_ID), "Call list ENTITY_TYPE_ID does not match in list"


@pytest.mark.dependency(name="test_calllist_list_as_list", depends=["test_calllist_add"])
def test_calllist_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.calllist.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    calllists = bitrix_response.result

    assert len(calllists) >= 1, "Expected at least one call list to be returned"

    for calllist in calllists:
        assert isinstance(calllist, dict)


@pytest.mark.dependency(name="test_calllist_list_as_list_fast", depends=["test_calllist_add"])
def test_calllist_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.calllist.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    calllists = bitrix_response.result

    last_calllist_id = None

    for calllist in calllists:
        assert isinstance(calllist, dict)
        assert "ID" in calllist

        calllist_id = int(calllist["ID"])

        if last_calllist_id is None:
            last_calllist_id = calllist_id
        else:
            assert last_calllist_id > calllist_id
            last_calllist_id = calllist_id
