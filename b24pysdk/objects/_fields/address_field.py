from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...schemas.address import Address
from .._filter_lookups import NO_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "AddressField",
]


class AddressField(BaseField[Text, Address]):
    """Field that exposes a Bitrix24 address string as ``Address``."""

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["AddressField", Optional[Address], List[Address]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[Address]:
        """Convert one raw Bitrix24 address string to an ``Address`` schema."""

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, str):
            raise TypeError(
                f"Field {self.attr_name!r} expects a string from Bitrix24, "
                f"got {type(value).__name__}.",
            )

        return Address.from_bitrix(value)

    def _convert_to_bitrix(self, value: Optional[Address]) -> Optional[Text]:
        """Convert one ``Address`` schema to a raw Bitrix24 address string."""

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, Address):
            raise TypeError(
                f"Field {self.attr_name!r} expects an Address instance, "
                f"got {type(value).__name__}.",
            )

        return value.to_bitrix()
