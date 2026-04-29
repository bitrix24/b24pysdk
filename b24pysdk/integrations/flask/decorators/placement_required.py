"""
Flask decorators and helpers for Bitrix24 placement request handling.

These helpers are intended for Flask endpoints that serve Bitrix24 widgets,
placements, slider applications, or other embedded app entry points.
"""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, TypeVar, Union, cast, overload

from flask import g

from ...._config import Config
from ....credentials import BitrixToken, OAuthPlacementData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ._utils import _make_json_response
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
    """Parse Bitrix24 placement auth payload from ``request.params``."""
    request.oauth_placement_data = OAuthPlacementData.from_dict(request.params)
    return cast("PlacementRequest", request)


def validate_placement_app_info_request(
    request: "PlacementRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "PlacementAppInfoRequest":
    """Resolve Bitrix24 ``app.info`` and validate the placement token against it."""

    try:
        bitrix_token = BitrixToken.from_oauth_placement_data(
            oauth_placement_data=request.oauth_placement_data,
            bitrix_app=bitrix_app,
        )
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
def placement_required(handler_func: _FT, /) -> _FT: ...


@overload
def placement_required(
    handler_func: None = None,
    /,
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
) -> Callable[[_FT], _FT]: ...


@overload
def placement_required(
    handler_func: None = None,
    /,
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
) -> Callable[[_FT], _FT]: ...


def placement_required(
    handler_func: Optional[_FT] = None,
    /,
    *,
    require_app_validation: bool = False,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Flask view that receives Bitrix24 placement requests.

    Error handling:
    - ``BitrixValidationError`` -> ``401 Unauthorized``
    - any other exception -> ``500 Internal Server Error``
    """

    if require_app_validation and bitrix_app is None:
        raise ValueError("'bitrix_app' is required when 'require_app_validation' is True")

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(*args: Any, **kwargs: Any):
            request = g.b24_request
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
                return _make_json_response({"error": error.message}, HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during placement request processing",
                    context={
                        "error": error.message,
                    },
                )
                return _make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 placement request processing",
                    context={
                        "error": str(error),
                    },
                )
                return _make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            return func(*args, **kwargs)

        return wrapper

    if handler_func is None:
        return decorator

    return decorator(handler_func)
