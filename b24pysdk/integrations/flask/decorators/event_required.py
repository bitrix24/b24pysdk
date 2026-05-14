"""Flask decorators and helpers for Bitrix24 event handlers."""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from flask import g

from ...._config import Config
from ....credentials import OAuthEventData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ....utils.types import JSONDict
from ..dependencies import get_request_params
from ._utils import make_json_response
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp

__all__ = [
    "event_required",
    "validate_event_params",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_event_params(
    params: JSONDict,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthEventData:
    """Parse Bitrix24 event payload from collected params and optionally validate it."""

    oauth_event_data = OAuthEventData.from_dict(params)

    if bitrix_app is not None:
        if oauth_event_data.is_system:
            raise BitrixValidationError(
                "System event cannot be validated via app.info",
            )

        try:
            app_info = oauth_event_data.get_app_info(bitrix_app)
        except BitrixAPIError as error:
            raise BitrixValidationError(error.message) from error

        if not (oauth_event_data.validate_against_app_info(app_info) and app_info.client_id == bitrix_app.client_id):
            raise BitrixValidationError("Invalid event auth data")

    return oauth_event_data


@overload
def event_required(
    handler_func: _FT,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _FT: ...


@overload
def event_required(
    handler_func: None = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Callable[[_FT], _FT]: ...


def event_required(
    handler_func: Optional[_FT] = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Flask view that receives Bitrix24 event callbacks.

    Error handling:
    - ``BitrixValidationError`` -> ``401 Unauthorized``
    - any other exception -> ``500 Internal Server Error``
    """

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(*args: Any, **kwargs: Any):
            try:
                g.oauth_event_data = validate_event_params(get_request_params(), bitrix_app=bitrix_app)

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 event request validation failed",
                    context={
                        "error": error.message,
                    },
                )
                return make_json_response({"error": error.message}, HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during event request processing",
                    context={
                        "error": error.message,
                    },
                )
                return make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 event request processing",
                    context={
                        "error": str(error),
                    },
                )
                return make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            return func(*args, **kwargs)

        return wrapper

    if handler_func is None:
        return decorator

    return decorator(handler_func)
