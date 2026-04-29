import json
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from django.http import HttpRequest

if TYPE_CHECKING:
    from ..types import CollectedParamsRequest

__all__ = [
    "collect_request_params",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def collect_request_params(view_func: _FT) -> _FT:
    """
    Collect Django request parameters into ``request.params``.

    This helper normalizes the most common request input channels used by
    Bitrix24 iframe handlers:

    1. JSON body from ``request.body``
    2. query-string data from ``request.GET``
    3. form data from ``request.POST``

    The resulting mapping is stored in ``request.params`` and the original
    request object is passed further down the decorator chain.

    Merge behavior
    --------------
    - JSON body is used as the initial mapping.
    - values from ``request.GET`` overwrite keys from the JSON body.
    - values from ``request.POST`` overwrite keys from JSON and query string.
    - multi-value keys are stored as ``list``.

    The function is idempotent: if ``request.params`` already exists, it is
    reused without rebuilding.

    References
    ----------
    - Django ``HttpRequest``:
      https://docs.djangoproject.com/en/stable/ref/request-response/#httprequest-objects
    - Django ``QueryDict``:
      https://docs.djangoproject.com/en/stable/ref/request-response/#querydict-objects
    """

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any):
        if hasattr(request, "params"):
            return view_func(request, *args, **kwargs)

        try:
            request.params = json.loads(request.body)
        except json.JSONDecodeError:
            request.params = {}

        for src in (request.GET, request.POST):
            for key, values in src.lists():
                request.params[key] = values if len(values) > 1 else values[0]

        return view_func(cast("CollectedParamsRequest", request), *args, **kwargs)

    return wrapper
