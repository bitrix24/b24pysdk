from typing import TYPE_CHECKING

from ...utils.types import JSONDict

if TYPE_CHECKING:
    from ...api.responses import B24AppInfoResult
    from ...credentials import OAuthEventData, OAuthPlacementData, OAuthWorkflowData

__all__ = [
    "CollectedParamsRequest",
    "EventAppInfoRequest",
    "EventRequest",
    "HasAppInfo",
    "PlacementAppInfoRequest",
    "PlacementRequest",
    "WorkflowAppInfoRequest",
    "WorkflowRequest",
]


class HasAppInfo:
    """Request mixin for views that already resolved ``app.info``."""

    app_info: "B24AppInfoResult"
    """Bitrix24 ``app.info`` response payload attached by a validation decorator."""


class CollectedParamsRequest:
    """
    Flask request normalized by ``collect_request_params``.

    The decorator reads data from ``flask.request`` and builds a dedicated SDK
    request object with normalized Bitrix24 parameters.
    """

    params: JSONDict
    """Normalized Bitrix24 request parameters collected from the incoming request."""

    def __init__(self, params: JSONDict):
        self.params = params


class PlacementRequest(CollectedParamsRequest):
    """Placement request with parsed ``OAuthPlacementData`` attached."""

    oauth_placement_data: "OAuthPlacementData"
    """Parsed Bitrix24 placement launch payload."""


class PlacementAppInfoRequest(PlacementRequest, HasAppInfo):
    """Placement request additionally validated against ``app.info``."""


class EventRequest(CollectedParamsRequest):
    """Event callback request with parsed ``OAuthEventData`` attached."""

    oauth_event_data: "OAuthEventData"
    """Parsed Bitrix24 event payload."""


class EventAppInfoRequest(EventRequest, HasAppInfo):
    """Event request additionally validated against ``app.info``."""


class WorkflowRequest(CollectedParamsRequest):
    """Workflow robot request with parsed ``OAuthWorkflowData`` attached."""

    oauth_workflow_data: "OAuthWorkflowData"
    """Parsed Bitrix24 workflow robot payload."""


class WorkflowAppInfoRequest(WorkflowRequest, HasAppInfo):
    """Workflow request additionally validated against ``app.info``."""
