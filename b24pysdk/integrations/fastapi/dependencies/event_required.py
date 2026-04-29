from http import HTTPStatus
from typing import TYPE_CHECKING, Literal, Optional, cast, overload

from fastapi import HTTPException
from starlette.requests import Request

from ...._config import Config
from ....credentials import BitrixToken, OAuthEventData
from ....errors import BitrixAPIError, BitrixSDKException, BitrixValidationError
from .collect_request_params import collect_request_params

if TYPE_CHECKING:
    from ....credentials import AbstractBitrixApp
    from ..types import CollectedParamsRequest, EventAppInfoRequest, EventRequest

__all__ = [
    "event_required",
    "validate_event_app_info_request",
    "validate_event_request",
]


def validate_event_request(request: "CollectedParamsRequest") -> "EventRequest":
    request.oauth_event_data = OAuthEventData.from_dict(request.params)
    return cast("EventRequest", request)


def validate_event_app_info_request(
    request: "EventRequest",
    *,
    bitrix_app: "AbstractBitrixApp",
) -> "EventAppInfoRequest":
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
def event_required(
    *,
    require_app_validation: Literal[False] = False,
    bitrix_app: None = None,
): ...


@overload
def event_required(
    *,
    require_app_validation: Literal[True],
    bitrix_app: "AbstractBitrixApp",
): ...


def event_required(
    *,
    require_app_validation: bool = False,
    bitrix_app: Optional["AbstractBitrixApp"] = None,
):
    if require_app_validation and bitrix_app is None:
        raise ValueError("'bitrix_app' is required when 'require_app_validation' is True")

    async def dependency(request: Request):
        try:
            validated_request = validate_event_request(await collect_request_params(request))

            if require_app_validation:
                validated_request = validate_event_app_info_request(validated_request, bitrix_app=bitrix_app)
        except BitrixValidationError as error:
            Config().logger.info("Bitrix24 event request validation failed", context={"error": error.message})
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=error.message) from error
        except BitrixSDKException as error:
            Config().logger.warning("Bitrix24 SDK error during event request processing", context={"error": error.message})
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error") from error
        except Exception as error:
            Config().logger.error("Unexpected error during Bitrix24 event request processing", context={"error": repr(error)})
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error") from error
        else:
            return validated_request

    return dependency
