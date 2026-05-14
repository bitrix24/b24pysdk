from typing import TYPE_CHECKING

from django.http import HttpRequest

if TYPE_CHECKING:
    from ...credentials import OAuthEventData, OAuthPlacementData, OAuthWorkflowData
    from ...utils.types import JSONDict

__all__ = [
    "CollectedParamsRequest",
    "EventRequest",
    "PlacementRequest",
    "WorkflowRequest",
]


class CollectedParamsRequest(HttpRequest):
    """
    Django request normalized by ``collect_request_params``.

    The decorator collects query string parameters, form data, and JSON body
    into a single ``request.params`` mapping so the next validation step can
    parse Bitrix24 payloads without inspecting transport details.
    """

    params: "JSONDict"
    """Normalized Bitrix24 request parameters collected from the incoming request."""


class PlacementRequest(CollectedParamsRequest):
    """Placement request with parsed ``OAuthPlacementData`` attached."""

    oauth_placement_data: "OAuthPlacementData"
    """Parsed Bitrix24 placement launch payload."""


class EventRequest(CollectedParamsRequest):
    """Event callback request with parsed ``OAuthEventData`` attached."""

    oauth_event_data: "OAuthEventData"
    """Parsed Bitrix24 event payload."""


class WorkflowRequest(CollectedParamsRequest):
    """Workflow robot request with parsed ``OAuthWorkflowData`` attached."""

    oauth_workflow_data: "OAuthWorkflowData"
    """Parsed Bitrix24 workflow robot payload."""
