from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import bool_from_bitrix, bool_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "BoolField",
]


class BoolField(BaseField[Union[bool, int, Text], bool]):
    """Field that exposes a Bitrix24 boolean-like value as ``bool``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["BoolField", Optional[bool], List[bool]]: ...

    def _convert_from_bitrix(self, value: Optional[Union[bool, int, Text]]) -> Optional[bool]:
        """Convert a single raw Bitrix24 boolean-like value to ``bool``."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return bool_from_bitrix(value, is_required=True)

        return bool_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[bool]) -> Optional[Text]:
        """Convert a single Python ``bool`` value to a Bitrix24 boolean value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return bool_to_bitrix(value, is_required=True)

        return bool_to_bitrix(value, is_required=False)
