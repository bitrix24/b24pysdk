from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from flask import g, request

if TYPE_CHECKING:
    from b24pysdk.utils.types import JSONDict

__all__ = [
    "collect_request_params",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def collect_request_params(handler_func: _FT) -> _FT:
    """
    Collect Flask request parameters into ``g.params``.

    This helper reads the current request from ``flask.request`` and stores a
    normalized mapping in ``flask.g.params`` for the wrapped handler.

    Merge behavior
    --------------
    - JSON body is used as the initial mapping.
    - values from ``request.args`` overwrite keys from the JSON body.
    - values from ``request.form`` overwrite keys from JSON and query string.
    - multi-value keys are stored as ``list``.

    The function is idempotent: if ``g.params`` already exists, it is reused
    without rebuilding.
    """

    @wraps(handler_func)
    def wrapper(*args: Any, **kwargs: Any):
        if not hasattr(g, "params"):
            params: "JSONDict" = {}

            request_json = request.get_json(silent=True)

            if isinstance(request_json, dict):
                params = request_json

            for source in (request.args, request.form):
                for key in source:
                    values = source.getlist(key)
                    params[key] = values if len(values) > 1 else values[0]

            g.params = params

        return handler_func(*args, **kwargs)

    return wrapper
