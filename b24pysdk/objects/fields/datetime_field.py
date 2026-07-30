from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import datetime_from_bitrix, datetime_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "DateTimeField",
]


class DateTimeField(BaseField[Text, datetime]):
    """Field that exposes a Bitrix24 datetime value as ``datetime``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["DateTimeField", Optional[datetime], List[datetime]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[datetime]:
        """Convert a single raw Bitrix24 datetime value to ``datetime``."""

        if self.is_required:
            if not value:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return datetime_from_bitrix(value, is_required=True)

        return datetime_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[datetime]) -> Optional[Text]:
        """Convert a single Python ``datetime`` value to a Bitrix24 datetime value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return datetime_to_bitrix(value, is_required=True)

        return datetime_to_bitrix(value, is_required=False)
