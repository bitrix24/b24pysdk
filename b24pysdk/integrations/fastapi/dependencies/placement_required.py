from http import HTTPStatus
from typing import TYPE_CHECKING, Literal, Optional, cast, overload

from fastapi import HTTPException
from starlette.requests import Request

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


def validate_placement_request(request: "CollectedParamsRequest") -> "PlacementRequest":
    request.oauth_placement_data = OAuthPlacementData.from_dict(request.params)
    return cast("PlacementRequest", request)


def validate_placement_app_info_request(
    request: "PlacementRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "PlacementAppInfoRequest":
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
def placement_required(
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
): ...


@overload
def placement_required(
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
): ...


def placement_required(
    *,
    require_app_validation: bool = False,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
):
    if require_app_validation and bitrix_app is None:
        raise ValueError("'bitrix_app' is required when 'require_app_validation' is True")

    async def dependency(request: Request):
        try:
            validated_request = validate_placement_request(await collect_request_params(request))

            if require_app_validation:
                validated_request = validate_placement_app_info_request(validated_request, bitrix_app=bitrix_app)
        except BitrixValidationError as error:
            Config().logger.info("Bitrix24 placement request validation failed", context={"error": error.message})
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=error.message) from error
        except BitrixSDKException as error:
            Config().logger.warning("Bitrix24 SDK error during placement request processing", context={"error": error.message})
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error") from error
        except Exception as error:
            Config().logger.error("Unexpected error during Bitrix24 placement request processing", context={"error": str(error)})
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error") from error
        else:
            return validated_request

    return dependency
