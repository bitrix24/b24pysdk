from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import int_from_bitrix, int_to_bitrix
from .._filter_lookups import ORDERED_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "IntField",
    "ListField",
]


class IntField(BaseField[Union[int, Text], int]):
    """Field that exposes a Bitrix24 int-like value as ``int``."""

    _FILTER_OPERATORS = ORDERED_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["IntField", Optional[int], List[int]]: ...

    def _convert_from_bitrix(self, value: Optional[Union[int, Text]]) -> Optional[int]:
        """Convert a single raw Bitrix24 int-like value to ``int``."""

        if self.is_required:
            if value is None or value == "":
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return int_from_bitrix(value, is_required=True)

        return int_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[int]) -> Optional[int]:
        """Convert a single Python ``int`` value to a Bitrix24 int value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return int_to_bitrix(value, is_required=True)

        return int_to_bitrix(value, is_required=False)


class ListField(IntField):
    """Bitrix24 list field that exposes selected item ID as ``int``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["ListField", Optional[int], List[int]]: ...
