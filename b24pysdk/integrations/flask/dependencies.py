from typing import TYPE_CHECKING, Any, Text, cast

from flask import g, has_app_context, has_request_context

from ...errors import BitrixSDKException

if TYPE_CHECKING:
    from ...credentials import OAuthEventData, OAuthPlacementData, OAuthWorkflowData
    from ...utils.types import JSONDict

__all__ = [
    "get_oauth_event_data",
    "get_oauth_placement_data",
    "get_oauth_workflow_data",
    "get_request_params",
]


def _get_required_g_value(name: Text, decorator_name: Text) -> Any:
    """
    Return a required value from ``flask.g``.

    Raises:
        BitrixSDKException: If there is no active Flask request context
            or the value was not prepared by the expected decorator.
    """

    if not (has_app_context() and has_request_context()):
        raise BitrixSDKException(
            f"Cannot access '{name}' outside Flask request context.",
        )

    if not hasattr(g, name):
        raise BitrixSDKException(
            f"Missing '{name}' in flask.g. "
            f"Make sure the route is wrapped with @{decorator_name}.",
        )

    return getattr(g, name)


def get_request_params() -> "JSONDict":
    """Return normalized request parameters stored by ``collect_request_params``."""
    return cast(
        "JSONDict",
        _get_required_g_value("params", "collect_request_params"),
    )


def get_oauth_placement_data() -> "OAuthPlacementData":
    """Return placement payload stored by ``placement_required``."""
    return cast(
        "OAuthPlacementData",
        _get_required_g_value("oauth_placement_data", "placement_required"),
    )


def get_oauth_event_data() -> "OAuthEventData":
    """Return event payload stored by ``event_required``."""
    return cast(
        "OAuthEventData",
        _get_required_g_value("oauth_event_data", "event_required"),
    )


def get_oauth_workflow_data() -> "OAuthWorkflowData":
    """Return workflow payload stored by ``workflow_required``."""
    return cast(
        "OAuthWorkflowData",
        _get_required_g_value("oauth_workflow_data", "workflow_required"),
    )
