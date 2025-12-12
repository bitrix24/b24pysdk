from typing import Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from tests.constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.bizproc,
    pytest.mark.robot,
]

_CODE: Text = f"{SDK_NAME.lower()}_test_robot"
_NAME: Text = f"{SDK_NAME} Test Robot"
_DESCRIPTION: Text = f"Test robot for {SDK_NAME}"
_HANDLER: Text = "https://example.com/robot_handler"
_UPDATED_HANDLER: Text = "https://example.com/robot_handler_updated"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Test Robot"

_PROPERTIES = {
    "inputField": {
        "Name": {
            "en": "Input field",
        },
        "Description": {
            "en": "Input field for robot processing",
        },
        "Type": "string",
        "Required": "Y",
        "Multiple": "N",
        "Default": "{=Document:NAME}",
    },
}

_RETURN_PROPERTIES = {
    "outputField": {
        "Name": {
            "en": "Robot Result",
        },
        "Type": "string",
        "Multiple": "N",
        "Default": None,
    },
}

_DOCUMENT_TYPE: Tuple[Text, Text, Text] = ("crm", "CCrmDocumentDeal", "DEAL")
_FILTER = {
    "INCLUDE": [
        ["crm"],
    ],
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_robot_add")
def test_bizproc_robot_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.bizproc.robot.add(
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

    is_added = cast(bool, bitrix_response.result)

    assert is_added is True, "Robot creation should return True"

    cache.set("robot_code", _CODE)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_robot_update", depends=["test_bizproc_robot_add"])
def test_bizproc_robot_update(bitrix_client: Client, cache: Cache):
    """"""

    robot_code = cache.get("robot_code", None)
    assert isinstance(robot_code, Text), "Robot code should be cached"

    bitrix_response = bitrix_client.bizproc.robot.update(
        code=robot_code,
        fields={
            "HANDLER": _UPDATED_HANDLER,
            "NAME": _UPDATED_NAME,
            "USE_SUBSCRIPTION": False,
            "FILTER": {
                "INCLUDE": [
                    ["crm"],
                    ["crm", "CCrmDocumentLead"],
                ],
            },
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "Robot update should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_robot_list", depends=["test_bizproc_robot_update"])
def test_bizproc_robot_list(bitrix_client: Client, cache: Cache):
    """"""

    robot_code = cache.get("robot_code", None)
    assert isinstance(robot_code, Text), "Robot code should be cached"

    bitrix_response = bitrix_client.bizproc.robot.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    robots = cast(list, bitrix_response.result)

    assert len(robots) == 1, "Expected one robot to be returned"

    robot = robots[0]

    assert isinstance(robot, Text)

    assert robot == robot_code


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_bizproc_robot_delete", depends=["test_bizproc_robot_list"])
def test_bizproc_robot_delete(bitrix_client: Client, cache: Cache):
    """"""

    robot_code = cache.get("robot_code", None)
    assert isinstance(robot_code, Text), "Robot code should be cached"

    bitrix_response = bitrix_client.bizproc.robot.delete(
        code=robot_code,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = cast(bool, bitrix_response.result)

    assert is_deleted is True, "Robot deletion should return True"
