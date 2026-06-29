from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIListResponse, BitrixAPIResponse, BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.utils.types import JSONDict

from ...constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.placement,
]

_PLACEMENT: Text = "PAGE_BACKGROUND_WORKER"
_HANDLER: Text = "https://example.com/handler/"
_LANG_ALL: JSONDict = {
    "en": {
        "TITLE": f"{SDK_NAME} TITLE",
        "DESCRIPTION": f"{SDK_NAME} DESCRIPTION",
        "GROUP_NAME": "",
    },
}
_OPTIONS: JSONDict = {
    "errorHandlerUrl": _HANDLER,
}
_USER_ID: int = BITRIX_PORTAL_OWNER_ID
_SCOPE: Text = "task"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_bind")
def test_placement_bind(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.bind(
        placement=_PLACEMENT,
        handler=_HANDLER,
        lang_all=_LANG_ALL,
        options=_OPTIONS,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_bound = bitrix_response.result

    assert is_bound is True, "Placement bind should return True"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_get", depends=["test_placement_bind"])
def test_placement_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    bound_placements = bitrix_response.result

    assert len(bound_placements) >= 1, "Expected at least one bound placement to be returned"

    for bound_placement in bound_placements:
        assert isinstance(bound_placement, dict)

        if all((
            bound_placement.get("placement") == _PLACEMENT,
            bound_placement.get("handler") == _HANDLER,
            bound_placement.get("langAll") == _LANG_ALL,
            bound_placement.get("options") == _OPTIONS,
            bound_placement.get("userId") == _USER_ID,
        )):
            break
    else:
        pytest.fail(f"Placement '{_PLACEMENT}' with handler '{_HANDLER}' should be found")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_get_as_list", depends=["test_placement_bind"])
def test_placement_get_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    bound_placements = bitrix_response.result

    assert len(bound_placements) >= 1, "Expected at least one bound placement to be returned"

    for bound_placement in bound_placements:
        assert isinstance(bound_placement, dict)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_list", depends=["test_placement_bind"])
def test_placement_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.list(scope=_SCOPE).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    placements = bitrix_response.result

    assert len(placements) >= 1, "Expected at least one placement in list to be returned"

    for placement in placements:
        assert isinstance(placement, str), "Placement should be a string"
        assert placement.startswith(f"{_SCOPE.upper()}_"), f"Placement should be prefixed with {_SCOPE.upper()}_"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_list_as_list", depends=["test_placement_bind"])
def test_placement_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    placements = bitrix_response.result

    assert len(placements) >= 1, "Expected at least one placement in list to be returned"

    for placement in placements:
        assert isinstance(placement, str), "Placement should be a string"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_placement_unbind", depends=["test_placement_bind"])
def test_placement_unbind(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.placement.unbind(
        placement=_PLACEMENT,
        handler=_HANDLER,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    unbind_count = bitrix_response.value

    assert isinstance(unbind_count, int), "Placement unbind count should be int"
    assert unbind_count > 0, "Placement unbind count should be positive"
