from functools import wraps
from typing import Any, Callable, TypeVar

from flask import g, request

from ..types import CollectedParamsRequest

__all__ = [
    "collect_request_params",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def collect_request_params(handler_func: _FT) -> _FT:
    """
    Collect Flask request parameters into ``g.b24_request.params``.

    This helper reads the current request from ``flask.request``, builds a
    dedicated SDK request object, stores it in ``flask.g.b24_request``, and
    leaves it available through ``flask.g`` for the wrapped handler.

    Merge behavior
    --------------
    - JSON body is used as the initial mapping.
    - values from ``request.args`` overwrite keys from the JSON body.
    - values from ``request.form`` overwrite keys from JSON and query string.
    - multi-value keys are stored as ``list``.

    The function is idempotent: if ``g.b24_request`` already exists, it is
    reused without rebuilding.
    """

    @wraps(handler_func)
    def wrapper(*args: Any, **kwargs: Any):
        if not hasattr(g, "b24_request"):
            params: dict[str, Any] = {}

            request_json = request.get_json(silent=True)
            if isinstance(request_json, dict):
                params = request_json

            for source in (request.args, request.form):
                for key in source:
                    values = source.getlist(key)
                    params[key] = values if len(values) > 1 else values[0]

            g.b24_request = CollectedParamsRequest(params=params)

        return handler_func(*args, **kwargs)

    return wrapper
