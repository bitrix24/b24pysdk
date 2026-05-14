from typing import TYPE_CHECKING, Annotated, Awaitable, Callable, Optional

from fastapi import Depends, HTTPException, status

from ...._config import Config
from ....credentials import OAuthEventData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ....utils.types import JSONDict
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp

__all__ = [
    "event_dependency",
    "get_event_dependency",
    "validate_event_params",
]


_EventDependency = Callable[..., Awaitable[OAuthEventData]]


def validate_event_params(
    params: JSONDict,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthEventData:
    """Parse Bitrix24 event payload from normalized params and optionally validate it."""

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

        if not (
            oauth_event_data.validate_against_app_info(app_info)
            and app_info.client_id == bitrix_app.client_id
        ):
            raise BitrixValidationError("Invalid event auth data")

    return oauth_event_data


def get_event_dependency(
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _EventDependency:
    """Create a FastAPI dependency that resolves Bitrix24 event payload."""

    async def _event_dependency(
            params: Annotated[JSONDict, Depends(collect_request_params)],
    ) -> OAuthEventData:
        try:
            return validate_event_params(
                params,
                bitrix_app=bitrix_app,
            )

        except BitrixValidationError as error:
            Config().logger.info(
                "Bitrix24 event request validation failed",
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
                "Bitrix24 SDK error during event request processing",
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
                "Unexpected error during Bitrix24 event request processing",
                context={
                    "error": str(error),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from error

    return _event_dependency


event_dependency: _EventDependency = get_event_dependency()
