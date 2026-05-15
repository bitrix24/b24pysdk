from typing import TYPE_CHECKING, Annotated, Awaitable, Callable, Optional

from fastapi import Depends, HTTPException, status

from ...._config import Config
from ....credentials import OAuthWorkflowData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ....utils.types import JSONDict
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp

__all__ = [
    "get_workflow_dependency",
    "validate_workflow_params",
    "workflow_dependency",
]


_WorkflowDependency = Callable[..., Awaitable[OAuthWorkflowData]]


def validate_workflow_params(
    params: JSONDict,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthWorkflowData:
    """
    Parse Bitrix24 workflow robot payload from normalized params.

    Args:
        params: Request parameters collected by ``collect_request_params``.
        bitrix_app: Optional SDK application object. When passed, the helper
            calls Bitrix24 ``app.info`` with workflow OAuth data and validates
            that the robot callback belongs to this application.

    Returns:
        Parsed workflow robot payload.
    """

    oauth_workflow_data = OAuthWorkflowData.from_dict(params)

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


def get_workflow_dependency(
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _WorkflowDependency:
    """
    Create a FastAPI dependency that resolves Bitrix24 workflow robot payload.

    Args:
        bitrix_app: Optional SDK application object. Pass it when the incoming
            workflow callback must be validated through Bitrix24 ``app.info``.
            If omitted, the dependency only parses and returns workflow data.
    """

    async def _workflow_dependency(params: Annotated[JSONDict, Depends(collect_request_params)]) -> OAuthWorkflowData:
        try:
            return validate_workflow_params(
                params,
                bitrix_app=bitrix_app,
            )

        except BitrixValidationError as error:
            Config().logger.info(
                "Bitrix24 workflow request validation failed",
                context={
                    "error": error.message,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error.message,
            ) from error

        except BitrixSDKException as error:
            Config().logger.warning(
                "Bitrix24 SDK error during workflow request processing",
                context={
                    "error": error.message,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from error

        except Exception as error:
            Config().logger.error(
                "Unexpected error during Bitrix24 workflow request processing",
                context={
                    "error": str(error),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from error

    return _workflow_dependency


workflow_dependency: _WorkflowDependency = get_workflow_dependency()
