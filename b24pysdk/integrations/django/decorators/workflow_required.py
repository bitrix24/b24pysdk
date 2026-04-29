"""
Django decorators and helpers for Bitrix24 workflow robot handlers.

References
----------
- Bitrix24 events:
  https://apidocs.bitrix24.com/api-reference/events/
- Django request / response API:
  https://docs.djangoproject.com/en/stable/ref/request-response/
"""

from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, TypeVar, Union, cast, overload

from django.http import JsonResponse

from ...._config import Config
from ....credentials import BitrixToken, OAuthWorkflowData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest, WorkflowAppInfoRequest, WorkflowRequest

__all__ = [
    "validate_app_info_workflow_data_request",
    "validate_workflow_data_request",
    "workflow_required",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_workflow_data_request(request: "CollectedParamsRequest") -> "WorkflowRequest":
    """
    Parse Bitrix24 workflow payload from ``request.params``.
    """
    request.oauth_workflow_data = OAuthWorkflowData.from_dict(request.params)
    return cast("WorkflowRequest", request)


def validate_app_info_workflow_data_request(
    request: "WorkflowRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "WorkflowAppInfoRequest":
    """
    Resolve Bitrix24 ``app.info`` and validate workflow robot auth payload.
    """

    if request.oauth_workflow_data.auth.oauth_token is None:
        raise BitrixValidationError("Workflow auth data does not contain OAuth token")

    try:
        bitrix_token = BitrixToken.from_oauth_workflow_data(oauth_workflow_data=request.oauth_workflow_data, bitrix_app=bitrix_app)
        app_info = bitrix_token.get_app_info().result
    except BitrixAPIError as error:
        raise BitrixValidationError(error.message) from error

    if not (
        request.oauth_workflow_data.validate_against_app_info(app_info)
        and app_info.client_id == bitrix_app.client_id
    ):
        raise BitrixValidationError("Invalid workflow auth data")

    request.app_info = app_info

    return cast("WorkflowAppInfoRequest", request)


@overload
def workflow_required(view_func: _FT, /) -> _FT: ...


@overload
def workflow_required(
    view_func: None = None,
    /,
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
) -> Callable[[_FT], _FT]: ...


@overload
def workflow_required(
    view_func: None = None,
    /,
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
) -> Callable[[_FT], _FT]: ...


def workflow_required(
    view_func: Optional[_FT] = None,
    /,
    *,
    require_app_validation: bool = False,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Django view that receives Bitrix24 workflow robot callbacks.

    Error handling:
    - ``BitrixValidationError`` -> ``401 Unauthorized``
    - any other exception -> ``500 Internal Server Error``
    """

    if require_app_validation and bitrix_app is None:
        raise ValueError("'bitrix_app' is required when 'require_app_validation' is True")

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(request: "CollectedParamsRequest", *args: Any, **kwargs: Any):
            try:
                request = validate_workflow_data_request(request)

                if require_app_validation:
                    request = validate_app_info_workflow_data_request(request, bitrix_app=bitrix_app)

            except BitrixValidationError as error:
                Config().logger.info(
                    "Bitrix24 workflow request validation failed",
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
                    "Unexpected error during Bitrix24 workflow request processing",
                    context={
                        "error": repr(error),
                    },
                )
                return JsonResponse({"error": "Internal server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            return func(request, *args, **kwargs)

        return wrapper

    if view_func is None:
        return decorator

    return decorator(view_func)
