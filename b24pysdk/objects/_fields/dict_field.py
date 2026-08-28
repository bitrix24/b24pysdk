from typing import TYPE_CHECKING, Optional, Type, Union

from ...utils.converters import dict_from_bitrix, dict_to_bitrix
from ...utils.types import JSONDict, JSONList
from .._filter_lookups import NO_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "DictField",
]


class DictField(BaseField[JSONDict, JSONDict]):
    """Field that exposes a Bitrix24 dictionary value as ``dict``."""

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["DictField", Optional[JSONDict], JSONList]: ...

    def _convert_from_bitrix(self, value: Optional[JSONDict]) -> Optional[JSONDict]:
        """Convert a single raw Bitrix24 dictionary value to ``dict``."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return dict_from_bitrix(value, is_required=True)

        return dict_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[JSONDict]) -> Optional[JSONDict]:
        """Convert a single Python ``dict`` value to a Bitrix24 dictionary value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return dict_to_bitrix(value, is_required=True)

        return dict_to_bitrix(value, is_required=False)
