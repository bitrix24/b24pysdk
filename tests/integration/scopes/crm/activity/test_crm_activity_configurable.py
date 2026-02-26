from datetime import datetime, timedelta
from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import (
    BitrixAPIResponse,
)
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24BoolLit
from b24pysdk.utils.types import JSONDict

from .....constants import SDK_NAME

pytestmark = [
    # pytest.mark.integration,
    # pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_configurable,
]

_FIELDS: Tuple[Text, ...] = ("activity", "time")

_OWNER_TYPE_ID: int = 1
_OWNER_ID: int = 1
_TYPE_ID: Text = "CONFIGURABLE"
_COMPLETED: B24BoolLit = B24BoolLit.FALSE
_DEADLINE: datetime = Config().get_local_datetime() + timedelta(days=1)
_PING_OFFSETS: list = [60, 300]
_IS_INCOMING_CHANNEL: B24BoolLit = B24BoolLit.FALSE
_RESPONSIBLE_ID: int = 1
_BADGE_CODE: Text = "b24pysdk_test_badge"
_ORIGINATOR_ID: Text = f"{SDK_NAME.lower()}_originator"
_ORIGIN_ID: Text = f"{SDK_NAME.lower()}_origin"

_UPDATED_COMPLETED: B24BoolLit = B24BoolLit.TRUE
_UPDATED_PING_OFFSETS: list = [300]
_UPDATED_RESPONSIBLE_ID: int = 2

_LAYOUT: JSONDict = {
    "icon": {
        "code": "call-completed",
    },
    "header": {
        "title": f"{SDK_NAME} Activity",
    },
    "body": {
        "logo": {
            "code": "call-incoming",
        },
        "blocks": {},
    },
    "footer": {
        "buttons": {
            "startCall": {
                "title": "About Client",
                "type": "primary",
                "action": {
                    "type": "openRestApp",
                    "actionParams": {
                        "clientId": "456",
                    },
                },
            },
        },
    },
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_timeline_activities_configurable_add")
def test_crm_activity_configurable_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.activity.configurable.add(
        owner_type_id=_OWNER_TYPE_ID,
        owner_id=_OWNER_ID,
        fields={
            "typeId": _TYPE_ID,
            "completed": _COMPLETED,
            "deadline": _DEADLINE.isoformat(),
            "pingOffsets": _PING_OFFSETS,
            "isIncomingChannel": _IS_INCOMING_CHANNEL,
            "responsibleId": _RESPONSIBLE_ID,
            "badgeCode": _BADGE_CODE,
            "originatorId": _ORIGINATOR_ID,
            "originId": _ORIGIN_ID,
        },
        layout=_LAYOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    activity = result["activity"]
    assert isinstance(activity, dict)

    activity_id = activity["id"]
    assert isinstance(activity_id, int)
    assert activity_id > 0

    cache.set("configurable_activity_id", activity_id)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_timeline_activities_configurable_get", depends=["test_crm_timeline_activities_configurable_add"])
def test_crm_activity_configurable_get(bitrix_client: BaseClient, cache: Cache):
    """"""
    activity_id = cache.get("configurable_activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.configurable.get(
        bitrix_id=activity_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    activity = result["activity"]

    assert isinstance(activity, dict)
    assert activity.get("id") == activity_id
    assert activity.get("ownerTypeId") == _OWNER_TYPE_ID
    assert activity.get("ownerId") == _OWNER_ID

    fields = activity["fields"]

    assert fields.get("typeId") == _TYPE_ID

    assert fields.get("completed") == bool(_COMPLETED)
    assert fields.get("isIncomingChannel") == bool(_IS_INCOMING_CHANNEL)
    assert fields.get("responsibleId") == _RESPONSIBLE_ID
    assert fields.get("badgeCode") == _BADGE_CODE
    assert fields.get("originatorId") == _ORIGINATOR_ID
    assert fields.get("originId") == _ORIGIN_ID
    assert fields.get("pingOffsets") == _PING_OFFSETS

    layout = activity["layout"]
    assert layout.get("header", {}).get("title") == _LAYOUT["header"]["title"]


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_timeline_activities_configurable_update", depends=["test_crm_timeline_activities_configurable_get"])
def test_crm_activity_configurable_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    activity_id = cache.get("configurable_activity_id", None)
    assert isinstance(activity_id, int)

    bitrix_response = bitrix_client.crm.activity.configurable.update(
        bitrix_id=activity_id,
        fields={
            "completed": _UPDATED_COMPLETED,
            "pingOffsets": _UPDATED_PING_OFFSETS,
            "responsibleId": _UPDATED_RESPONSIBLE_ID,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result
    activity = result["activity"]
    assert isinstance(activity, dict)

    assert activity.get("id") == activity_id
