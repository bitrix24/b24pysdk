from typing import TYPE_CHECKING, cast

from flask import g

if TYPE_CHECKING:
    from ...credentials import OAuthEventData, OAuthPlacementData, OAuthWorkflowData
    from ...utils.types import JSONDict

__all__ = [
    "get_oauth_event_data",
    "get_oauth_placement_data",
    "get_oauth_workflow_data",
    "get_request_params",
]


def get_request_params() -> "JSONDict":
    """Return normalized Bitrix24 request parameters stored in ``flask.g``."""
    return cast("JSONDict", g.params)


def get_oauth_placement_data() -> "OAuthPlacementData":
    """Return placement payload stored in ``flask.g`` by ``placement_required``."""
    return cast("OAuthPlacementData", g.oauth_placement_data)


def get_oauth_event_data() -> "OAuthEventData":
    """Return event payload stored in ``flask.g`` by ``event_required``."""
    return cast("OAuthEventData", g.oauth_event_data)


def get_oauth_workflow_data() -> "OAuthWorkflowData":
    """Return workflow payload stored in ``flask.g`` by ``workflow_required``."""
    return cast("OAuthWorkflowData", g.oauth_workflow_data)
