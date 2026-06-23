from abc import ABC
from dataclasses import dataclass
from typing import Annotated, Generic, List, Optional, Text, TypedDict, TypeVar, Union, overload

from ..constants import B24AppStatus
from ..utils.converters import bool_from_bitrix, bool_to_bitrix
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import B24BoolStrictLiteral
from ._base_schema import BaseSchema

__all__ = [
    "AppInfo",
    "AppInfoApplication",
    "AppInfoApplicationData",
    "AppInfoBase",
    "AppInfoData",
    "AppInfoWebhook",
    "AppInfoWebhookData",
]


class _AppInfoBaseData(TypedDict):
    LICENSE: Text


class AppInfoApplicationData(_AppInfoBaseData):
    ID: int
    CODE: Text
    VERSION: int
    STATUS: Text
    INSTALLED: bool
    PAYMENT_EXPIRED: Annotated[Text, B24BoolStrictLiteral]
    DAYS: Optional[int]
    LANGUAGE_ID: Text
    LICENSE_TYPE: Text
    LICENSE_FAMILY: Text


class AppInfoWebhookData(_AppInfoBaseData):
    SCOPE: List[Text]


AppInfoData = Union[AppInfoApplicationData, AppInfoWebhookData]

_AppInfoDataT = TypeVar("_AppInfoDataT", bound=AppInfoData)


@dataclass(**frozen_dataclass_kwargs())
class AppInfoBase(BaseSchema[_AppInfoDataT], ABC, Generic[_AppInfoDataT]):
    """
    Result returned by the ``app.info`` method.

    The response format depends on the authorization context. Incoming
    webhooks return scope and license information, while applications return
    extended application information.
    """

    license: Text

    @overload
    @classmethod
    def from_bitrix(cls, bitrix_data: AppInfoApplicationData, /) -> "AppInfoApplication": ...

    @overload
    @classmethod
    def from_bitrix(cls, bitrix_data: AppInfoWebhookData, /) -> "AppInfoWebhook": ...

    @classmethod
    def from_bitrix(cls, bitrix_data: _AppInfoDataT, /) -> Union["AppInfoApplication", "AppInfoWebhook"]:
        """
        Create an appropriate AppInfo schema from Bitrix24 app.info data.

        Args:
            bitrix_data: Raw ``result`` object returned by the
                ``app.info`` method.

        Returns:
            AppInfoWebhook or AppInfoApplication schema depending on the
            response structure.
        """
        if "ID" in bitrix_data:
            return AppInfoApplication.from_bitrix(bitrix_data)
        else:
            return AppInfoWebhook.from_bitrix(bitrix_data)


@dataclass(**frozen_dataclass_kwargs())
class AppInfoApplication(AppInfoBase[AppInfoApplicationData]):
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
            bitrix_id=bitrix_data["ID"],
            code=bitrix_data["CODE"],
            version=bitrix_data["VERSION"],
            status=B24AppStatus(bitrix_data["STATUS"]),
            installed=bitrix_data["INSTALLED"],
            payment_expired=bool_from_bitrix(bitrix_data["PAYMENT_EXPIRED"], is_required=True),
            days=bitrix_data["DAYS"],
            language_id=bitrix_data["LANGUAGE_ID"],
            license=bitrix_data["LICENSE"],
            license_type=bitrix_data["LICENSE_TYPE"],
            license_family=bitrix_data["LICENSE_FAMILY"],
        )

    def to_bitrix(self) -> AppInfoApplicationData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with extended application information.
        """
        return {
            "ID": self.bitrix_id,
            "CODE": self.code,
            "VERSION": self.version,
            "STATUS": self.status.value,
            "INSTALLED": self.installed,
            "PAYMENT_EXPIRED": bool_to_bitrix(self.payment_expired, is_required=True),
            "DAYS": self.days,
            "LANGUAGE_ID": self.language_id,
            "LICENSE": self.license,
            "LICENSE_TYPE": self.license_type,
            "LICENSE_FAMILY": self.license_family,
        }


@dataclass(**frozen_dataclass_kwargs())
class AppInfoWebhook(AppInfoBase[AppInfoWebhookData]):
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
            license=bitrix_data["LICENSE"],
            scope=bitrix_data["SCOPE"],
        )

    def to_bitrix(self) -> AppInfoWebhookData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with webhook application information.
        """
        return {
            "SCOPE": self.scope,
            "LICENSE": self.license,
        }


AppInfo = Union[AppInfoApplication, AppInfoWebhook]
