from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import float_from_bitrix, float_to_bitrix
from .._filter_lookups import ORDERED_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "FloatField",
]


class FloatField(BaseField[Union[int, float, Text], float]):
    """Field that exposes a Bitrix24 float-like value as ``float``."""

    _FILTER_OPERATORS = ORDERED_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["FloatField", Optional[float], List[float]]: ...

    def _convert_from_bitrix(self, value: Optional[Union[int, float, Text]]) -> Optional[float]:
        """Convert a single raw Bitrix24 float-like value to ``float``."""

        if self.is_required:
            if value is None or value == "":
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return float_from_bitrix(value, is_required=True)

        return float_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[Union[int, float]]) -> Optional[float]:
        """Convert a single Python number value to a Bitrix24 float value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return float_to_bitrix(value, is_required=True)

        return float_to_bitrix(value, is_required=False)
