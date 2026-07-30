from typing import TYPE_CHECKING, List, Optional, Text, Type, Union
from zoneinfo import ZoneInfo

from ...utils.converters import timezone_from_bitrix, timezone_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "TimeZoneField",
]


class TimeZoneField(BaseField[Text, ZoneInfo]):
    """Field that exposes a Bitrix24 timezone value as ``ZoneInfo``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["TimeZoneField", Optional[ZoneInfo], List[ZoneInfo]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[ZoneInfo]:
        """Convert a single raw Bitrix24 timezone value to ``ZoneInfo``."""

        if self.is_required:
            if not value:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return timezone_from_bitrix(value, is_required=True)

        return timezone_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[ZoneInfo]) -> Optional[Text]:
        """Convert a single Python ``ZoneInfo`` value to a Bitrix24 timezone value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return timezone_to_bitrix(value, is_required=True)

        return timezone_to_bitrix(value, is_required=False)
