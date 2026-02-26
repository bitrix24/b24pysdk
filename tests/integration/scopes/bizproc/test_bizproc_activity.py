from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from tests.constants import SDK_NAME

pytestmark = [
    # pytest.mark.integration,
    pytest.mark.bizproc,
    pytest.mark.activity,
]

_CODE: Text = f"{SDK_NAME.lower()}_test_activity"
_NAME: Text = f"{SDK_NAME} Test Activity"
_DESCRIPTION: Text = f"Test activity for {SDK_NAME}"
_HANDLER: Text = "https://example.com/handler"
_UPDATED_HANDLER: Text = "https://example.com/handler_updated"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Test Activity"
_LOG_MESSAGE: Text = f"{SDK_NAME} test log message"

_PROPERTIES = {
    "inputString": {
        "Name": {
            "en": "Input string",
        },
        "Description": {
            "en": "Input string for processing",
        },
        "Type": "string",
        "Required": "Y",
        "Multiple": "N",
        "Default": "{=Document:NAME}",
    },
}

_RETURN_PROPERTIES = {
    "outputString": {
        "Name": {
            "en": "Result",
        },
        "Type": "string",
        "Multiple": "N",
        "Default": None,
    },
}

_DOCUMENT_TYPE: Tuple[Text, Text, Text] = ("lists", "BizprocDocument", "iblock_164")
_FILTER = {
    "INCLUDE": [
        ["lists"],
    ],
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_activity_add")
def test_bizproc_activity_add(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.bizproc.activity.add(
        code=_CODE,
        handler=_HANDLER,
        name=_NAME,
        description=_DESCRIPTION,
        properties=_PROPERTIES,
        return_properties=_RETURN_PROPERTIES,
        document_type=_DOCUMENT_TYPE,
        filter=_FILTER,
        use_subscription=True,
        use_placement=False,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_added = bitrix_response.result

    assert is_added is True, "Activity creation should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_activity_update", depends=["test_bizproc_activity_add"])
def test_bizproc_activity_update(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.bizproc.activity.update(
        code=_CODE,
        fields={
            "HANDLER": _UPDATED_HANDLER,
            "NAME": _UPDATED_NAME,
            "USE_SUBSCRIPTION": False,
            "FILTER": {
                "INCLUDE": [
                    ["lists"],
                    ["crm", "CCrmDocumentDeal"],
                ],
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result

    assert is_updated is True, "Activity update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_activity_list", depends=["test_bizproc_activity_update"])
def test_bizproc_activity_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.bizproc.activity.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    activities = bitrix_response.result

    assert len(activities) == 1, "Expected one activity to be returned"

    activity = activities[0]

    assert isinstance(activity, Text)

    assert activity == _CODE

# @pytest.mark.oauth_only
# def test_bizproc_activity_log(bitrix_client: BaseClient):
#     """"""
#
#     test_event_token = "test_token_12345"
#
#     bitrix_response = bitrix_client.bizproc.activity.log(
#         event_token=test_event_token,
#         log_message=_LOG_MESSAGE,
#     ).response
#
#     assert isinstance(bitrix_response, BitrixAPIResponse)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_activity_delete", depends=["test_bizproc_activity_list"])
def test_bizproc_activity_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    activity_code = cache.get("activity_code", None)
    assert isinstance(activity_code, Text), "Activity code should be cached"

    bitrix_response = bitrix_client.bizproc.activity.delete(
        code=activity_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Activity deletion should return True"
