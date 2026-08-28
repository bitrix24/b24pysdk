from enum import Enum
from typing import Any, Generic, Optional, Text, Type, TypeVar

from .base_field import BaseField

__all__ = [
    "EnumField",
]

_BEnumT = TypeVar("_BEnumT", bound=Enum)


class EnumField(BaseField[Any, _BEnumT], Generic[_BEnumT]):
    """Field that exposes a Bitrix24 raw value as a stdlib ``Enum`` member."""

    __slots__ = ("_enum_class",)

    _enum_class: Type[_BEnumT]

    def __init__(
            self,
            bitrix_code: Text,
            *,
            enum_class: Type[_BEnumT],
            is_pk: bool = False,
            is_required: bool = False,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_missing_allowed: bool = False,
    ):
        if not issubclass(enum_class, Enum):
            raise TypeError("enum_class must be a Enum subclass.")

        super().__init__(
            bitrix_code=bitrix_code,
            is_pk=is_pk,
            is_required=is_required,
            is_multiple=is_multiple,
            is_read_only=is_read_only,
            is_missing_allowed=is_missing_allowed,
        )
        self._enum_class = enum_class

    def _convert_from_bitrix(self, value: Optional[Any]) -> Optional[_BEnumT]:
        """Convert a raw Bitrix24 value to an enum member."""

        if value is None or value == "":
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        return self._enum_class(value)

    def _convert_to_bitrix(self, value: Optional[_BEnumT]) -> Optional[Any]:
        """Convert an enum member to a Bitrix24 value."""

        if value is None:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, self._enum_class):
            raise TypeError(
                f"Field {self.attr_name!r} expects an instance of "
                f"{self._enum_class.__name__}, got {type(value).__name__}.",
            )

        return value.value
