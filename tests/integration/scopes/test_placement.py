from typing import Text, cast

import pytest

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.utils.types import JSONDict

from ...constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.placement,
]

_PLACEMENT: Text = "TASK_VIEW_TAB"
_HANDLER: Text = "https://example.com/handler/"
_LANG_ALL: JSONDict = {
    "en": {
        "TITLE": f"{SDK_NAME} TITLE",
        "DESCRIPTION": f"{SDK_NAME} DESCRIPTION",
        "GROUP_NAME": "",
    },
}
_UNBIND_RESULT_FIELD: Text = "count"
_SCOPE: Text = "task"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_bind")
def test_placement_bind(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.bind(
        placement=_PLACEMENT,
        handler=_HANDLER,
        lang_all=_LANG_ALL,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_bound = cast(bool, bitrix_response.result)

    assert is_bound is True, "Placement bind should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_get", depends=["test_placement_bind"])
def test_placement_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    bound_placements = cast(list, bitrix_response.result)

    assert len(bound_placements) >= 1, "Expected at least one bound placement to be returned"

    bound_placement = bound_placements[0]

    assert isinstance(bound_placement, dict)

    assert bound_placement.get("placement") == _PLACEMENT, "Placement name does not match"
    assert bound_placement.get("handler") == _HANDLER, "Placement handler does not match"
    assert bound_placement.get("langAll") == _LANG_ALL, "Placement lang_all does not match"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_get_as_list", depends=["test_placement_bind"])
def test_placement_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    bound_placements = cast(list, bitrix_response.result)

    assert len(bound_placements) >= 1, "Expected at least one bound placement to be returned"

    for bound_placement in bound_placements:
        assert isinstance(bound_placement, dict)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_list", depends=["test_placement_bind"])
def test_placement_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.list(scope=_SCOPE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    placements = cast(list, bitrix_response.result)

    assert len(placements) >= 1, "Expected at least one placement in list to be returned"

    for placement in placements:
        assert isinstance(placement, str), "Placement should be a string"
        assert placement.startswith(f"{_SCOPE.upper()}_"), f"Placement should be prefixed with {_SCOPE.upper()}_"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_list_as_list", depends=["test_placement_bind"])
def test_placement_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    placements = cast(list, bitrix_response.result)

    assert len(placements) >= 1, "Expected at least one placement in list to be returned"

    for placement in placements:
        assert isinstance(placement, str), "Placement should be a string"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_unbind", depends=["test_placement_get_as_list"])
def test_placement_unbind(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.placement.unbind(
        placement=_PLACEMENT,
        handler=_HANDLER,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    unbind_result = cast(dict, bitrix_response.result)

    assert _UNBIND_RESULT_FIELD in unbind_result, f"Field {_UNBIND_RESULT_FIELD!r} should be present"

    unbind_count = unbind_result[_UNBIND_RESULT_FIELD]

    assert isinstance(unbind_count, int), f"Field '{_UNBIND_RESULT_FIELD}' should be an integer"
    assert unbind_count > 0, "Unbind count should be positive"
