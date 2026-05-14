"""Flask decorators and helpers for Bitrix24 workflow robot handlers."""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from flask import g

from ...._config import Config
from ....credentials import OAuthWorkflowData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ....utils.types import JSONDict
from ..dependencies import get_request_params
from ._utils import make_json_response
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp

__all__ = [
    "validate_workflow_params",
    "workflow_required",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_workflow_params(
    params: JSONDict,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthWorkflowData:
    """Parse Bitrix24 workflow payload from collected params and optionally validate it."""

    oauth_workflow_data = OAuthWorkflowData.from_dict(params)

    if bitrix_app is not None:
        try:
            app_info = oauth_workflow_data.get_app_info(bitrix_app)
        except BitrixAPIError as error:
            raise BitrixValidationError(error.message) from error

        if not (oauth_workflow_data.validate_against_app_info(app_info) and app_info.client_id == bitrix_app.client_id):
            raise BitrixValidationError("Invalid workflow auth data")

    return oauth_workflow_data


@overload
def workflow_required(
    handler_func: _FT,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _FT: ...


@overload
def workflow_required(
    handler_func: None = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Callable[[_FT], _FT]: ...


def workflow_required(
    handler_func: Optional[_FT] = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Flask view that receives Bitrix24 workflow robot callbacks.

    Error handling:
    - ``BitrixValidationError`` -> ``401 Unauthorized``
    - any other exception -> ``500 Internal Server Error``
    """

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(*args: Any, **kwargs: Any):
            try:
                g.oauth_workflow_data = validate_workflow_params(get_request_params(), bitrix_app=bitrix_app)

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 workflow request validation failed",
                    context={
                        "error": error.message,
                    },
                )
                return make_json_response({"error": error.message}, HTTPStatus.UNAUTHORIZED)

            except BitrixSDKException as error:
                Config().logger.warning(
                    "Bitrix24 SDK error during workflow request processing",
                    context={
                        "error": error.message,
                    },
                )
                return make_json_response({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 workflow request processing",
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
