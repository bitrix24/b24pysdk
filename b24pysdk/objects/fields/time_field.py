from datetime import time
from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import time_from_bitrix, time_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "TimeField",
]


class TimeField(BaseField[Text, time]):
    """Field that exposes a Bitrix24 time value as ``time``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["TimeField", Optional[time], List[time]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[time]:
        """Convert a single raw Bitrix24 time value to ``time``."""

        if self.is_required:
            if not value:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return time_from_bitrix(value, is_required=True)

        return time_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[time]) -> Optional[Text]:
        """Convert a single Python ``time`` value to a Bitrix24 time value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return time_to_bitrix(value, is_required=True)

        return time_to_bitrix(value, is_required=False)
