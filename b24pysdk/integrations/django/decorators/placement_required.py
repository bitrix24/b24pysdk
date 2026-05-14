"""
Django decorators and helpers for Bitrix24 placement request handling.

These helpers are intended for Django endpoints that serve Bitrix24 widgets,
placements, slider applications, or other embedded app entry points.

References
----------
- Bitrix24 widgets / placements:
  https://apidocs.bitrix24.com/api-reference/widgets/
- Django request / response API:
  https://docs.djangoproject.com/en/stable/ref/request-response/
"""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from django.http import JsonResponse

from ...._config import Config
from ....credentials import OAuthPlacementData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest

__all__ = [
    "placement_required",
    "validate_placement_request",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_placement_request(
        request: "CollectedParamsRequest",
        *,
        bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthPlacementData:
    """
    Parse Bitrix24 placement auth payload from ``request.params``.

    Parameters
    ----------
    request:
        Django request already normalized by
        :func:`collect_request_params`. The request must contain
        ``request.params`` with the Bitrix24 placement launch payload.

    bitrix_app:
        SDK application object used to call ``app.info`` and validate that
        the placement payload belongs to the expected application. If omitted,
        only payload parsing is performed.

    Returns
    -------
    OAuthPlacementData
        Parsed Bitrix24 placement launch payload.

    Raises
    ------
    BitrixValidationError
        Raised when ``request.params`` does not contain a valid Bitrix24
        placement payload for :class:`b24pysdk.credentials.OAuthPlacementData`.

    Notes
    -----
    This function always parses Bitrix24 placement parameters. When
    ``bitrix_app`` is passed, it also resolves ``app.info`` and validates
    placement data against it.

    Typical placement fields
    ------------------------
    The exact payload depends on the embedding context, but Bitrix24 placement
    launch data usually contains keys such as:

    - ``DOMAIN``
    - ``PROTOCOL``
    - ``LANG``
    - ``APP_SID``
    - ``member_id``
    - ``status``
    - OAuth access / refresh token fields passed to the placement iframe

    See the Bitrix24 placement documentation for context:
    https://apidocs.bitrix24.com/api-reference/widgets/
    """

    oauth_placement_data = OAuthPlacementData.from_dict(request.params)

    if bitrix_app is not None:

        try:
            app_info = oauth_placement_data.get_app_info(bitrix_app)
        except BitrixAPIError as error:
            raise BitrixValidationError(error.message) from error

        if not (
                oauth_placement_data.validate_against_app_info(app_info)
                and app_info.client_id == bitrix_app.client_id
        ):
            raise BitrixValidationError("Invalid placement auth data")

    return oauth_placement_data


@overload
def placement_required(
    view_func: _FT,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _FT: ...


@overload
def placement_required(
    view_func: None = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Callable[[_FT], _FT]: ...


def placement_required(
    view_func: Optional[_FT] = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Django view that receives Bitrix24 placement requests.

    Parameters
    ----------
    view_func:
        Django view function. The decorator supports both forms:

        - ``@placement_required``
        - ``@placement_required(...)``

    bitrix_app:
        Optional SDK app object. If passed, the decorator additionally
        resolves Bitrix24 ``app.info`` and verifies the placement payload
        against the current application.

    Returns
    -------
    Callable
        Wrapped Django view function.

    Error handling
    --------------
    The decorator converts errors into HTTP responses using the following
    policy:

    - :class:`BitrixValidationError` -> ``401 Unauthorized``
    - any other :class:`Exception` -> ``500 Internal Server Error``

    This design keeps helper functions reusable from starter applications while
    still giving the decorator a safe default HTTP behavior.

    Processing steps
    ----------------
    1. Collect all request parameters into ``request.params`` using
       :func:`collect_request_params`.
    2. Parse placement payload with :func:`validate_placement_request`.
    3. Optionally validate ``app.info`` inside
       :func:`validate_placement_request`.
    4. Call the wrapped Django view with the enriched request object.

    Examples
    --------
    Parse placement payload only:

    .. code-block:: python

        @placement_required
        def widget_view(request):
            return JsonResponse({"domain": request.oauth_placement_data.domain})

    Parse placement payload and verify it against the current app:

    .. code-block:: python

        @placement_required(bitrix_app=bitrix_app)
        def widget_view(request):
            return JsonResponse({
                "domain": request.oauth_placement_data.domain,
            })
    """

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(request: "CollectedParamsRequest", *args: Any, **kwargs: Any):
            try:
                request.oauth_placement_data = validate_placement_request(
                    request,
                    bitrix_app=bitrix_app,
                )

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 placement request validation failed",
                    context={
                        "error": error.message,
                    },
                )
                return JsonResponse({"error": error.message}, status=HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during placement request processing",
                    context={
                        "error": error.message,
                    },
                )
                return JsonResponse({"error": "Internal server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 placement request processing",
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
