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
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from django.http import JsonResponse

from ...._config import Config
from ....credentials import OAuthWorkflowData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest

__all__ = [
    "validate_workflow_request",
    "workflow_required",
]

_FT = TypeVar("_FT", bound=Callable[..., Any])


def validate_workflow_request(
        request: "CollectedParamsRequest",
        *,
        bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthWorkflowData:
    """
    Parse Bitrix24 workflow payload from ``request.params``.

    Parameters
    ----------
    request:
        Django request already normalized by
        :func:`collect_request_params`. The request must contain
        ``request.params`` with the Bitrix24 workflow robot payload.

    bitrix_app:
        SDK application object used to call ``app.info`` and validate that
        the workflow payload belongs to the expected application. If omitted,
        only payload parsing is performed.

    Returns
    -------
    OAuthWorkflowData
        Parsed Bitrix24 workflow robot payload.

    Raises
    ------
    BitrixValidationError
        Raised when ``request.params`` does not contain a valid Bitrix24
        workflow payload for :class:`b24pysdk.credentials.OAuthWorkflowData`.

    Notes
    -----
    This function always parses Bitrix24 workflow parameters. When
    ``bitrix_app`` is passed, it also resolves ``app.info`` and validates
    workflow data against it.

    Typical workflow fields
    -----------------------
    Workflow robot payloads usually include keys such as:

    - ``workflow_id``
    - ``code``
    - ``document_id``
    - ``document_type``
    - ``event_token``
    - ``auth[...]``

    See the Bitrix24 event documentation for context:
    https://apidocs.bitrix24.com/api-reference/events/
    """
    oauth_workflow_data = OAuthWorkflowData.from_dict(request.params)

    if bitrix_app is not None:
        try:
            app_info = oauth_workflow_data.get_app_info(bitrix_app)
        except BitrixAPIError as error:
            raise BitrixValidationError(error.message) from error

        if not (
                oauth_workflow_data.validate_against_app_info(app_info)
                and app_info.client_id == bitrix_app.client_id
        ):
            raise BitrixValidationError("Invalid workflow auth data")

    return oauth_workflow_data


@overload
def workflow_required(
    view_func: _FT,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _FT: ...


@overload
def workflow_required(
    view_func: None = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Callable[[_FT], _FT]: ...


def workflow_required(
    view_func: Optional[_FT] = None,
    /,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> Union[_FT, Callable[[_FT], _FT]]:
    """
    Decorate a Django view that receives Bitrix24 workflow robot callbacks.

    Parameters
    ----------
    view_func:
        Django view function. The decorator supports both forms:

        - ``@workflow_required``
        - ``@workflow_required(...)``

    bitrix_app:
        Optional SDK app object. If passed, the decorator additionally
        resolves Bitrix24 ``app.info`` and verifies the workflow payload
        against the current application.

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
    2. Parse workflow payload with :func:`validate_workflow_request`.
    3. Optionally validate ``app.info`` inside
       :func:`validate_workflow_request`.
    4. Call the wrapped Django view with the enriched request object.

    Examples
    --------
    Parse workflow payload only:

    .. code-block:: python

        @workflow_required
        def workflow_view(request):
            return JsonResponse({
                "workflow_id": request.oauth_workflow_data.workflow_id,
            })

    Parse workflow payload and verify it against the current app:

    .. code-block:: python

        @workflow_required(bitrix_app=bitrix_app)
        def workflow_view(request):
            return JsonResponse({
                "workflow_id": request.oauth_workflow_data.workflow_id,
            })
    """

    def decorator(func: _FT) -> _FT:
        @wraps(func)
        @collect_request_params
        def wrapper(request: "CollectedParamsRequest", *args: Any, **kwargs: Any):
            try:
                request.oauth_workflow_data = validate_workflow_request(
                    request,
                    bitrix_app=bitrix_app,
                )

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
                    "Bitrix24 SDK error during workflow request processing",
                    context={
                        "error": error.message,
                    },
                )
                return JsonResponse({"error": "Internal server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            except Exception as error:  # noqa: BLE001
                Config().logger.error(
                    "Unexpected error during Bitrix24 workflow request processing",
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
