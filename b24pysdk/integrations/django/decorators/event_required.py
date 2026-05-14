"""
Django decorators and helpers for Bitrix24 event and workflow handlers.

References
----------
- Bitrix24 events:
  https://apidocs.bitrix24.com/api-reference/events/
- Django request / response API:
  https://docs.djangoproject.com/en/stable/ref/request-response/
"""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from django.http import JsonResponse

from ...._config import Config
from ....credentials import OAuthEventData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest

__all__ = [
    "event_required",
    "validate_event_request",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_event_request(
        request: "CollectedParamsRequest",
        *,
        bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthEventData:
    """
    Parse Bitrix24 event payload from ``request.params``.

    Parameters
    ----------
    request:
        Django request already normalized by
        :func:`collect_request_params`. The request must contain
        ``request.params`` with the Bitrix24 event callback payload.

    bitrix_app:
        SDK application object used to call ``app.info`` and validate that
        the event payload belongs to the expected application. If omitted,
        only payload parsing is performed.

    Returns
    -------
    OAuthEventData
        Parsed Bitrix24 event callback payload.

    Raises
    ------
    BitrixValidationError
        Raised when ``request.params`` does not contain a valid Bitrix24 event
        payload for :class:`b24pysdk.credentials.OAuthEventData`.

    Notes
    -----
    This function always parses Bitrix24 event parameters. When
    ``bitrix_app`` is passed, it also resolves ``app.info`` and validates
    event data against it.

    Typical event fields
    --------------------
    Event callback payloads usually include keys such as:

    - ``event``
    - ``event_handler_id``
    - ``data[FIELDS][...]``
    - ``ts``
    - ``auth[...]``

    See the Bitrix24 event documentation for context:
    https://apidocs.bitrix24.com/api-reference/events/
    """
    oauth_event_data = OAuthEventData.from_dict(request.params)

    if bitrix_app is not None:
        if oauth_event_data.is_system:
            raise BitrixValidationError(
                "System event cannot be validated via app.info",
            )

        try:
            app_info = oauth_event_data.get_app_info(bitrix_app)
        except BitrixAPIError as error:
            raise BitrixValidationError(error.message) from error

        if not (
                oauth_event_data.validate_against_app_info(app_info)
                and app_info.client_id == bitrix_app.client_id
        ):
            raise BitrixValidationError("Invalid event auth data")

    return oauth_event_data


@overload
def event_required(
    view_func: _FT,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _FT: ...


@overload
def event_required(
    view_func: None = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Callable[[_FT], _FT]: ...


def event_required(
    view_func: Optional[_FT] = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Django view that receives Bitrix24 event callbacks.

    Parameters
    ----------
    view_func:
        Django view function. The decorator supports both forms:

        - ``@event_required``
        - ``@event_required(...)``

    bitrix_app:
        Optional SDK app object. If passed, the decorator additionally
        resolves Bitrix24 ``app.info`` and verifies the event payload against
        the current application.

    Returns
    -------
    Callable
        Wrapped Django view function.

    Error handling:
    - ``BitrixValidationError`` -> ``401 Unauthorized``
    - any other exception -> ``500 Internal Server Error``

    Processing steps
    ----------------
    1. Collect all request parameters into ``request.params`` using
       :func:`collect_request_params`.
    2. Parse event payload with :func:`validate_event_request`.
    3. Optionally validate ``app.info`` inside
       :func:`validate_event_request`.
    4. Call the wrapped Django view with the enriched request object.

    Examples
    --------
    Parse event payload only:

    .. code-block:: python

        @event_required
        def event_view(request):
            return JsonResponse({"event": request.oauth_event_data.event})

    Parse event payload and verify it against the current app:

    .. code-block:: python

        @event_required(bitrix_app=bitrix_app)
        def event_view(request):
            return JsonResponse({
                "event": request.oauth_event_data.event,
            })
    """

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(request: "CollectedParamsRequest", *args: Any, **kwargs: Any):
            try:
                request.oauth_event_data = validate_event_request(
                    request,
                    bitrix_app=bitrix_app,
                )

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 event request validation failed",
                    context={
                        "error": error.message,
                    },
                )
                return JsonResponse({"error": error.message}, status=HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during event request processing",
                    context={
                        "error": error.message,
                    },
                )
                return JsonResponse({"error": "Internal server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 event request processing",
                    context={
                        "error": str(error),
                    },
                )
                return JsonResponse({"error": "Internal server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            return func(request, *args, **kwargs)

        return wrapper

    if view_func is None:
        return decorator

    return decorator(view_func)
