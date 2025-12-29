from datetime import datetime, timedelta
from typing import Generator, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import (
    BitrixAPIListFastResponse,
    BitrixAPIListResponse,
    BitrixAPIResponse,
)
from b24pysdk.constants import B24BoolLit
from b24pysdk.utils.types import JSONDictGenerator

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_only,
]

_FIELDS: Tuple[Text, ...] = ("ID", "OWNER_TYPE_ID", "OWNER_ID", "TYPE_ID", "SUBJECT", "RESPONSIBLE_ID")

_OWNER_TYPE_ID: int = 1
_OWNER_ID: int = 43
_TYPE_ID: int = 2
_SUBJECT: Text = f"{SDK_NAME} Activity Subject"
_RESPONSIBLE_ID: int = 1
_COMPLETED: B24BoolLit = B24BoolLit.FALSE
_START_TIME: datetime = Config().get_local_datetime() + timedelta(days=1)
_END_TIME: datetime = _START_TIME + timedelta(hours=1)
_DESCRIPTION: Text = f"{SDK_NAME} Activity Description"
_COMMUNICATIONS_VALUE: Text = f"+{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
_COMMUNICATIONS_ENTITY_ID: int = 1
_COMMUNICATIONS_ENTITY_TYPE_ID: int = 3

_UPDATED_SUBJECT: Text = f"Updated {SDK_NAME} Activity Subject"
_UPDATED_RESPONSIBLE_ID: int = 2
_UPDATED_DESCRIPTION: Text = f"Updated {SDK_NAME} Activity Description"


def test_crm_activity_fields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_activity_add")
def test_crm_activity_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.activity.add(
        fields={
            "OWNER_TYPE_ID": _OWNER_TYPE_ID,
            "OWNER_ID": _OWNER_ID,
            "TYPE_ID": _TYPE_ID,
            "SUBJECT": _SUBJECT,
            "RESPONSIBLE_ID": _RESPONSIBLE_ID,
            "COMPLETED": _COMPLETED,
            "START_TIME": _START_TIME.isoformat(),
            "END_TIME": _END_TIME.isoformat(),
            "DESCRIPTION": _DESCRIPTION,
            "COMMUNICATIONS": [
                {
                    "VALUE": _COMMUNICATIONS_VALUE,
                    "ENTITY_ID": _COMMUNICATIONS_ENTITY_ID,
                    "ENTITY_TYPE_ID": _COMMUNICATIONS_ENTITY_TYPE_ID,
                },
            ],
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    activity_id = cast(int, bitrix_response.result)
    assert isinstance(activity_id, int)
    assert activity_id > 0

    cache.set("activity_id", activity_id)


@pytest.mark.dependency(name="test_crm_activity_get", depends=["test_crm_activity_add"])
def test_crm_activity_get(bitrix_client: Client, cache: Cache):
    """"""

    activity_id = cache.get("activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.get(
        bitrix_id=activity_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    activity = cast(dict, bitrix_response.result)

    assert activity.get("ID") == str(activity_id)
    assert activity.get("OWNER_TYPE_ID") == str(_OWNER_TYPE_ID)
    assert activity.get("OWNER_ID") == str(_OWNER_ID)
    assert activity.get("TYPE_ID") == str(_TYPE_ID)
    assert activity.get("SUBJECT") == _SUBJECT
    assert activity.get("RESPONSIBLE_ID") == str(_RESPONSIBLE_ID)
    assert activity.get("COMPLETED") == _COMPLETED
    assert _DESCRIPTION in activity.get("DESCRIPTION")


@pytest.mark.dependency(name="test_crm_activity_list", depends=["test_crm_activity_get"])
def test_crm_activity_list(bitrix_client: Client, cache: Cache):
    """"""

    activity_id = cache.get("activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.list(
        select=list(_FIELDS),
        filter={"ID": activity_id},
        order={"ID": "desc"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    activities = cast(list, bitrix_response.result)

    for activity in activities:
        assert isinstance(activity, dict)
        if all((
            activity.get("ID") == str(activity_id),
            activity.get("OWNER_TYPE_ID") == str(_OWNER_TYPE_ID),
            activity.get("OWNER_ID") == str(_OWNER_ID),
            activity.get("TYPE_ID") == str(_TYPE_ID),
            activity.get("SUBJECT") == _SUBJECT,
            activity.get("RESPONSIBLE_ID") == str(_RESPONSIBLE_ID),
        )):
            break
    else:
        pytest.fail(f"Test activity with ID {activity_id} should be found in list")


@pytest.mark.dependency(name="test_crm_activity_list_as_list", depends=["test_crm_activity_list"])
def test_crm_activity_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    activities = cast(list, bitrix_response.result)

    assert len(activities) >= 1, "Expected at least one activity to be returned"

    for activity in activities:
        assert isinstance(activity, dict)


@pytest.mark.dependency(name="test_crm_activity_list_as_list_fast", depends=["test_crm_activity_list_as_list"])
def test_crm_activity_list_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    activities = cast(JSONDictGenerator, bitrix_response.result)

    last_activity_id = None

    for activity in activities:
        assert isinstance(activity, dict)
        assert "ID" in activity

        current_activity_id = int(activity["ID"])

        if last_activity_id is None:
            last_activity_id = current_activity_id
        else:
            assert last_activity_id > current_activity_id
            last_activity_id = current_activity_id


@pytest.mark.dependency(name="test_crm_activity_update", depends=["test_crm_activity_list_as_list_fast"])
def test_crm_activity_update(bitrix_client: Client, cache: Cache):
    """"""

    activity_id = cache.get("activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.update(
        bitrix_id=activity_id,
        fields={
            "SUBJECT": _UPDATED_SUBJECT,
            "RESPONSIBLE_ID": _UPDATED_RESPONSIBLE_ID,
            "DESCRIPTION": _UPDATED_DESCRIPTION,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)
    assert is_updated is True


@pytest.mark.dependency(name="test_crm_activity_delete", depends=["test_crm_activity_update"])
def test_crm_activity_delete(bitrix_client: Client, cache: Cache):
    """"""

    activity_id = cache.get("activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.delete(
        bitrix_id=activity_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = cast(bool, bitrix_response.result)
    assert is_deleted is True
