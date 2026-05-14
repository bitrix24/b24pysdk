"""
FastAPI dependencies and helpers for Bitrix24 placement request handling.

These helpers are intended for FastAPI endpoints that serve Bitrix24 widgets,
placements, slider applications, or other embedded app entry points.

References
----------
- Bitrix24 widgets / placements:
  https://apidocs.bitrix24.com/api-reference/widgets/
- FastAPI dependencies:
  https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from typing import TYPE_CHECKING, Annotated, Awaitable, Callable, Optional

from fastapi import Depends, HTTPException, status

from ...._config import Config
from ....credentials import OAuthPlacementData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from ....utils.types import JSONDict
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp

__all__ = [
    "get_placement_dependency",
    "placement_dependency",
    "validate_placement_params",
]


_PlacementDependency = Callable[..., Awaitable[OAuthPlacementData]]


def validate_placement_params(
    params: JSONDict,
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> OAuthPlacementData:
    """Parse Bitrix24 placement auth payload from normalized params and optionally validate it."""

    oauth_placement_data = OAuthPlacementData.from_dict(params)

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


def get_placement_dependency(
    *,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
) -> _PlacementDependency:
    """Create a FastAPI dependency that resolves Bitrix24 placement payload."""

    async def _placement_dependency(
            params: Annotated[JSONDict, Depends(collect_request_params)],
    ) -> OAuthPlacementData:
        try:
            return validate_placement_params(
                params,
                bitrix_app=bitrix_app,
            )

        except BitrixValidationError as error:
            Config().logger.info(
                "Bitrix24 placement request validation failed",
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
                "Bitrix24 SDK error during placement request processing",
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
                "Unexpected error during Bitrix24 placement request processing",
                context={
                    "error": str(error),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from error

    return _placement_dependency


placement_dependency: _PlacementDependency = get_placement_dependency()
