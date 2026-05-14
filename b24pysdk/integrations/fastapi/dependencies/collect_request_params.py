import json

from fastapi import Request

from ....utils.types import JSONDict

__all__ = [
    "collect_request_params",
]


async def collect_request_params(request: Request) -> JSONDict:
    """Collect FastAPI request parameters into a normalized mapping."""

    params: JSONDict = {}

    try:
        request_json = await request.json()

        if isinstance(request_json, dict):
            params.update(request_json)

    except json.JSONDecodeError:
        pass

    for source in (request.query_params, await request.form()):
        for key in source:
            values = source.getlist(key)
            params[key] = values if len(values) > 1 else values[0]

    return params
