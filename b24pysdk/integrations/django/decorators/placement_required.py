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
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, TypeVar, Union, cast, overload

from django.http import JsonResponse

from ...._config import Config
from ....credentials import BitrixToken, OAuthPlacementData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest, PlacementAppInfoRequest, PlacementRequest

__all__ = [
    "placement_required",
    "validate_placement_app_info_request",
    "validate_placement_request",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_placement_request(request: "CollectedParamsRequest") -> "PlacementRequest":
    """
    Parse Bitrix24 placement auth payload from ``request.params``.

    Parameters
    ----------
    request:
        Django request already normalized by
        :func:`collect_request_params`. The request must contain
        ``request.params`` with the Bitrix24 placement launch payload.

    Returns
    -------
    PlacementRequest
        The same Django request instance with
        ``request.oauth_placement_data`` attached.

    Raises
    ------
    BitrixValidationError
        Raised when ``request.params`` does not contain a valid Bitrix24
        placement payload for :class:`b24pysdk.credentials.OAuthPlacementData`.

    Notes
    -----
    This function performs only the first stage of validation:

    1. Parse Bitrix24 placement parameters.
    2. Store parsed placement data in ``request.oauth_placement_data``.

    It does not call ``app.info`` and does not verify that the placement token
    belongs to a specific Bitrix24 application. For that second step, use
    :func:`validate_app_info_placement_data_request`.

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
    request.oauth_placement_data = OAuthPlacementData.from_dict(request.params)
    return cast("PlacementRequest", request)


def validate_placement_app_info_request(
    request: "PlacementRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "PlacementAppInfoRequest":
    """
    Resolve Bitrix24 ``app.info`` and validate the placement token against it.

    Parameters
    ----------
    request:
        Request previously returned by
        :func:`validate_placement_data_request`. The request must already
        contain ``request.oauth_placement_data``.
    bitrix_app:
        SDK application object representing the current Bitrix24 app.
        Its ``client_id`` is used to verify that the resolved placement token
        belongs to the expected application.

    Returns
    -------
    PlacementAppInfoRequest
        The same Django request instance with ``request.app_info`` attached.

    Raises
    ------
    BitrixValidationError
        Raised when:

        - the placement payload does not match the resolved ``app.info``
        - the resolved ``app.info.client_id`` does not match
          ``bitrix_app.client_id``
        - Bitrix24 returns :class:`BitrixAPIError` while resolving ``app.info``

    Validation flow
    ---------------
    1. Build :class:`BitrixToken` from ``request.oauth_placement_data``.
    2. Call Bitrix24 ``app.info`` using the placement token.
    3. Validate placement data against ``app_info.install``.
    4. Validate the resolved ``client_id`` against ``bitrix_app.client_id``.
    5. Store the resolved app info in ``request.app_info``.

    References
    ----------
    - Bitrix24 widgets / placements:
      https://apidocs.bitrix24.com/api-reference/widgets/
    - Bitrix24 common settings reference:
      https://apidocs.bitrix24.com/api-reference/common/settings/index.html
    """

    try:
        bitrix_token = BitrixToken.from_oauth_placement_data(oauth_placement_data=request.oauth_placement_data, bitrix_app=bitrix_app)
        app_info = bitrix_token.get_app_info().result
    except BitrixAPIError as error:
        raise BitrixValidationError(error.message) from error

    if not (
        request.oauth_placement_data.validate_against_app_info(app_info)
        and app_info.client_id == bitrix_app.client_id
    ):
        raise BitrixValidationError("Invalid placement auth data")

    request.app_info = app_info

    return cast("PlacementAppInfoRequest", request)


@overload
def placement_required(view_func: _FT, /) -> _FT: ...


@overload
def placement_required(
    view_func: None = None,
    /,
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
) -> Callable[[_FT], _FT]: ...


@overload
def placement_required(
    view_func: None = None,
    /,
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
) -> Callable[[_FT], _FT]: ...


def placement_required(
    view_func: Optional[_FT] = None,
    /,
    *,
    require_app_validation: bool = False,
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

    require_app_validation:
        Controls whether the decorator performs only placement parsing or the
        full validation flow.

        - ``False``: build ``request.params`` and parse
          ``request.oauth_placement_data`` only.
        - ``True``: additionally resolve Bitrix24 ``app.info`` and attach
          ``request.app_info`` after verification.

    bitrix_app:
        Required when ``require_app_validation=True``. This is the SDK app
        object representing the Bitrix24 application expected to own the
        current placement token.

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
    2. Parse placement payload with
       :func:`validate_placement_data_request`.
    3. Optionally validate ``app.info`` with
       :func:`validate_app_info_placement_data_request`.
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

        @placement_required(
            require_app_validation=True,
            bitrix_app=bitrix_app,
        )
        def widget_view(request):
            return JsonResponse({
                "domain": request.oauth_placement_data.domain,
                "client_id": request.app_info.client_id,
            })
    """

    if require_app_validation and bitrix_app is None:
        raise ValueError("'bitrix_app' is required when 'require_app_validation' is True")

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(request: "CollectedParamsRequest", *args: Any, **kwargs: Any):
            try:
                request = validate_placement_request(request)

                if require_app_validation:
                    request = validate_placement_app_info_request(request, bitrix_app=bitrix_app)

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
