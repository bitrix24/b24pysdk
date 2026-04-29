"""Flask decorators and helpers for Bitrix24 event handlers."""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, TypeVar, Union, cast, overload

from flask import g

from ...._config import Config
from ....credentials import BitrixToken, OAuthEventData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ._utils import _make_json_response
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest, EventAppInfoRequest, EventRequest

__all__ = [
    "event_required",
    "validate_event_app_info_request",
    "validate_event_request",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_event_request(request: "CollectedParamsRequest") -> "EventRequest":
    """Parse Bitrix24 event payload from ``request.params``."""
    request.oauth_event_data = OAuthEventData.from_dict(request.params)
    return cast("EventRequest", request)


def validate_event_app_info_request(
    request: "EventRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "EventAppInfoRequest":
    """Resolve Bitrix24 ``app.info`` and validate event auth payload."""

    if request.oauth_event_data.auth.oauth_token is None:
        raise BitrixValidationError("System event auth data cannot be validated via app.info without external installation context")

    try:
        bitrix_token = BitrixToken.from_oauth_event_data(
            oauth_event_data=request.oauth_event_data,
            bitrix_app=bitrix_app,
        )
        app_info = bitrix_token.get_app_info().result
    except BitrixAPIError as error:
        raise BitrixValidationError(error.message) from error

    if not (
        request.oauth_event_data.validate_against_app_info(app_info)
        and app_info.client_id == bitrix_app.client_id
    ):
        raise BitrixValidationError("Invalid event auth data")

    request.app_info = app_info

    return cast("EventAppInfoRequest", request)


@overload
def event_required(handler_func: _FT, /) -> _FT: ...


@overload
def event_required(
    handler_func: None = None,
    /,
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
) -> Callable[[_FT], _FT]: ...


@overload
def event_required(
    handler_func: None = None,
    /,
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
) -> Callable[[_FT], _FT]: ...


def event_required(
    handler_func: Optional[_FT] = None,
    /,
    *,
    require_app_validation: bool = False,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Flask view that receives Bitrix24 event callbacks.

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
                request = validate_event_request(request)

                if require_app_validation:
                    request = validate_event_app_info_request(request, bitrix_app=bitrix_app)

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 event request validation failed",
                    context={
                        "error": error.message,
                    },
                )
                return _make_json_response({"error": error.message}, HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during event request processing",
                    context={
                        "error": error.message,
                    },
                )
                return _make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 event request processing",
                    context={
                        "error": repr(error),
                    },
                )
                return _make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            return func(*args, **kwargs)

        return wrapper

    if handler_func is None:
        return decorator

    return decorator(handler_func)
