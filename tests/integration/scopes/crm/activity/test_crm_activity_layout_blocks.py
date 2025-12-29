from typing import cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse
from b24pysdk.utils.types import JSONDict

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_activity,
    pytest.mark.crm_activity_layout_blocks,
]

_ENTITY_TYPE_ID: int = 1
_ENTITY_ID: int = 43
_ACTIVITY_ID: int = 89

_LAYOUT: JSONDict = {
    "blocks": {
        "block_1": {
            "type": "text",
            "properties": {
                "value": f"{SDK_NAME} Hello!\nWe are starting.",
                "multiline": True,
                "bold": True,
                "color": "base_90",
            },
        },
        "block_2": {
            "type": "largeText",
            "properties": {
                "value": f"{SDK_NAME} Hello!\nWe are starting.\nWe are continuing.",
            },
        },
        "block_3": {
            "type": "link",
            "properties": {
                "text": f"{SDK_NAME} Open deal",
                "bold": True,
                "action": {
                    "type": "redirect",
                    "uri": f"/crm/lead/details/{_ENTITY_ID}/",
                },
            },
        },
    },
}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_layout_blocks_set")
def test_crm_activity_layout_blocks_set(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.layout.blocks.set(
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_ENTITY_ID,
        activity_id=_ACTIVITY_ID,
        layout=_LAYOUT,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    assert result == {"success": True}


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_layout_blocks_get", depends=["test_crm_activity_layout_blocks_set"])
def test_crm_activity_layout_blocks_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.layout.blocks.get(
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_ENTITY_ID,
        activity_id=_ACTIVITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    assert isinstance(result, dict)
    assert "layout" in result

    layout = cast(dict, result["layout"])
    assert isinstance(layout, dict)
    assert "blocks" in layout

    blocks = cast(dict, layout["blocks"])

    assert "block_1" in blocks
    assert blocks["block_1"]["type"] == "text"
    assert blocks["block_1"]["properties"]["value"].startswith(f"{SDK_NAME} Hello!")

    assert "block_2" in blocks
    assert blocks["block_2"]["type"] == "largeText"

    assert "block_3" in blocks
    assert blocks["block_3"]["type"] == "link"
    assert blocks["block_3"]["properties"]["text"].startswith(f"{SDK_NAME} Open")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_activity_layout_blocks_delete", depends=["test_crm_activity_layout_blocks_get"])
def test_crm_activity_layout_blocks_delete(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.activity.layout.blocks.delete(
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_ENTITY_ID,
        activity_id=_ACTIVITY_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    assert result == {"success": True}
