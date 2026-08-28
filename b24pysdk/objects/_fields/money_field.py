from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...schemas.money import Money
from .._filter_lookups import ORDERED_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "MoneyField",
]


class MoneyField(BaseField[Text, Money]):
    """Field that exposes a Bitrix24 money string as ``Money``."""

    _FILTER_OPERATORS = ORDERED_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["MoneyField", Optional[Money], List[Money]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[Money]:
        """Convert one raw Bitrix24 money string to a ``Money`` schema."""

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, str):
            raise TypeError(
                f"Field {self.attr_name!r} expects a string from Bitrix24, "
                f"got {type(value).__name__}.",
            )

        return Money.from_bitrix(value)

    def _convert_to_bitrix(self, value: Optional[Money]) -> Optional[Text]:
        """Convert one ``Money`` schema to a raw Bitrix24 money string."""

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, Money):
            raise TypeError(
                f"Field {self.attr_name!r} expects a Money instance, "
                f"got {type(value).__name__}.",
            )

        return value.to_bitrix()
