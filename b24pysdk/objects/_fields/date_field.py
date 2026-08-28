from datetime import date
from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import date_from_bitrix, date_to_bitrix
from .._filter_lookups import ORDERED_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "DateField",
]


class DateField(BaseField[Text, date]):
    """Field that exposes a Bitrix24 date value as ``date``."""

    _FILTER_OPERATORS = ORDERED_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["DateField", Optional[date], List[date]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[date]:
        """Convert a single raw Bitrix24 date value to ``date``."""

        if self.is_required:
            if not value:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return date_from_bitrix(value, is_required=True)

        return date_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[date]) -> Optional[Text]:
        """Convert a single Python ``date`` value to a Bitrix24 date value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return date_to_bitrix(value, is_required=True)

        return date_to_bitrix(value, is_required=False)
