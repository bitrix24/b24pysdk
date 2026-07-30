from abc import ABC
from dataclasses import dataclass
from typing import Annotated, Generic, List, Optional, Text, TypedDict, TypeVar, Union

from ..constants import B24AppStatus
from ..utils.converters import (
    bool_from_bitrix,
    bool_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import B24AppStatusLiteral, B24BoolStrictLiteral
from ._base_schema import BaseSchema

__all__ = [
    "AppInfo",
    "AppInfoApplication",
    "AppInfoApplicationData",
    "AppInfoData",
    "AppInfoWebhook",
    "AppInfoWebhookData",
]


class _BaseAppInfoData(TypedDict):
    LICENSE: Text


class AppInfoApplicationData(_BaseAppInfoData):
    ID: int
    CODE: Text
    VERSION: int
    STATUS: Annotated[Text, B24AppStatusLiteral]
    INSTALLED: bool
    PAYMENT_EXPIRED: Annotated[Text, B24BoolStrictLiteral]
    DAYS: Optional[int]
    LANGUAGE_ID: Text
    LICENSE_TYPE: Text
    LICENSE_FAMILY: Text


class AppInfoWebhookData(_BaseAppInfoData):
    SCOPE: List[Text]


AppInfoData = Union[AppInfoApplicationData, AppInfoWebhookData]

_AppInfoDataT = TypeVar("_AppInfoDataT", bound=AppInfoData)


@dataclass(**frozen_dataclass_kwargs())
class _BaseAppInfo(BaseSchema[_AppInfoDataT], ABC, Generic[_AppInfoDataT]):
    """
    Result returned by the ``app.info`` method.

    The response format depends on the authorization context. Incoming
    webhooks return scope and license information, while applications return
    extended application information.
    """
    license: Text


@dataclass(**frozen_dataclass_kwargs())
class AppInfoApplication(_BaseAppInfo[AppInfoApplicationData]):
    """
    Information returned by ``app.info`` in the application context.
    """

    bitrix_id: int
    code: Text
    version: int
    status: B24AppStatus
    installed: bool
    payment_expired: bool
    days: Optional[int]
    language_id: Text
    license_type: Text
    license_family: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: AppInfoApplicationData, /) -> "AppInfoApplication":
        """
        Create an AppInfoApplication schema from Bitrix24 app.info data.

        Args:
            bitrix_data: Raw application ``result`` object returned by the
                ``app.info`` method.

        Returns:
            AppInfoApplication schema.
        """
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            code=text_from_bitrix(bitrix_data["CODE"], is_required=True),
            version=int_from_bitrix(bitrix_data["VERSION"], is_required=True),
            status=B24AppStatus(bitrix_data["STATUS"]),
            installed=bool_from_bitrix(bitrix_data["INSTALLED"], is_required=True),
            payment_expired=bool_from_bitrix(bitrix_data["PAYMENT_EXPIRED"], is_required=True),
            days=int_from_bitrix(bitrix_data["DAYS"]),
            language_id=text_from_bitrix(bitrix_data["LANGUAGE_ID"], is_required=True),
            license=text_from_bitrix(bitrix_data["LICENSE"], is_required=True),
            license_type=text_from_bitrix(bitrix_data["LICENSE_TYPE"], is_required=True),
            license_family=text_from_bitrix(bitrix_data["LICENSE_FAMILY"], is_required=True),
        )

    def to_bitrix(self) -> AppInfoApplicationData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with extended application information.
        """
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "CODE": text_to_bitrix(self.code, is_required=True),
            "VERSION": int_to_bitrix(self.version, is_required=True),
            "STATUS": self.status.value,
            "INSTALLED": bool_from_bitrix(self.installed, is_required=True),
            "PAYMENT_EXPIRED": bool_to_bitrix(self.payment_expired, is_required=True),
            "DAYS": int_to_bitrix(self.days),
            "LANGUAGE_ID": text_to_bitrix(self.language_id, is_required=True),
            "LICENSE": text_to_bitrix(self.license, is_required=True),
            "LICENSE_TYPE": text_to_bitrix(self.license_type, is_required=True),
            "LICENSE_FAMILY": text_to_bitrix(self.license_family, is_required=True),
        }


@dataclass(**frozen_dataclass_kwargs())
class AppInfoWebhook(_BaseAppInfo[AppInfoWebhookData]):
    """
    Information returned by ``app.info`` for an incoming webhook.
    """

    scope: List[Text]

    @classmethod
    def from_bitrix(cls, bitrix_data: AppInfoWebhookData, /) -> "AppInfoWebhook":
        """
        Create an AppInfoWebhook schema from Bitrix24 app.info data.

        Args:
            bitrix_data: Raw webhook ``result`` object returned by the
                ``app.info`` method.

        Returns:
            AppInfoWebhook schema.
        """
        return cls(
            license=text_from_bitrix(bitrix_data["LICENSE"], is_required=True),
            scope=[
                text_from_bitrix(scope, is_required=True)
                for scope in bitrix_data["SCOPE"]
            ],
        )

    def to_bitrix(self) -> AppInfoWebhookData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with webhook application information.
        """
        return {
            "SCOPE": [
                text_to_bitrix(scope, is_required=True)
                for scope in self.scope
            ],
            "LICENSE": text_to_bitrix(self.license, is_required=True),
        }


AppInfo = Union[AppInfoApplication, AppInfoWebhook]
