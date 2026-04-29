import json
from typing import TYPE_CHECKING, Any, cast

from starlette.requests import Request

if TYPE_CHECKING:
    from ..types import CollectedParamsRequest

__all__ = [
    "collect_request_params",
]


async def collect_request_params(request: Request) -> "CollectedParamsRequest":
    """Collect FastAPI request parameters into ``request.params``."""

    if hasattr(request, "params"):
        return cast("CollectedParamsRequest", request)

    params: dict[str, Any] = {}

    try:
        request_json = await request.json()
        if isinstance(request_json, dict):
            params = request_json
    except (json.JSONDecodeError, TypeError, ValueError):
        params = {}

    for source in (request.query_params, await request.form()):
        for key in source:
            values = source.getlist(key)
            params[key] = values if len(values) > 1 else values[0]

    request.params = params

    return cast("CollectedParamsRequest", request)
