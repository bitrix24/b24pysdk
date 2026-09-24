from enum import Enum
from typing import TYPE_CHECKING, Generic, Iterable, List, Optional, Text, Type, TypeVar, Union

from ...utils.types import cast
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "EnumField",
]

_BEnumT = TypeVar("_BEnumT", bound=Enum)
_BEnumValue = Union[Text, int]


class EnumField(BaseField[_BEnumValue, _BEnumT], Generic[_BEnumT]):
    """Field that exposes a Bitrix24 raw value as a stdlib ``Enum`` member."""

    __slots__ = ("_enum_class",)

    _enum_class: Type[_BEnumT]

    def __init__(
            self,
            bitrix_code: Text,
            *,
            enum_class: Type[_BEnumT],
            is_pk: bool = False,
            is_required: Optional[bool] = None,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_updatable: bool = True,
            request_name: Optional[Text] = None,
    ):
        if not (isinstance(enum_class, type) and issubclass(enum_class, Enum)):
            raise TypeError("enum_class must be an Enum subclass.")

        super().__init__(
            bitrix_code=bitrix_code,
            is_pk=is_pk,
            is_required=is_required,
            is_multiple=is_multiple,
            is_read_only=is_read_only,
            is_updatable=is_updatable,
            request_name=request_name,
        )
        self._enum_class = enum_class

    @property
    def enum_class(self) -> Type[_BEnumT]:
        """Return the immutable enum class used by this field."""
        return self._enum_class

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["EnumField[_BEnumT]", Optional[_BEnumT], List[_BEnumT]]: ...

        def __set__(
                self,
                instance: Optional["BaseObject"],
                value: Union[Optional[Union[_BEnumT, _BEnumValue]], Iterable[Union[_BEnumT, _BEnumValue]]],
        ): ...

    def _convert_from_bitrix(self, value: Optional[_BEnumValue]) -> Optional[_BEnumT]:
        """Convert a raw Bitrix24 value to an enum member."""

        if value is None or value == "":
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        return self._enum_class(value)

    def _convert_to_bitrix(self, value: Optional[Union[_BEnumT, _BEnumValue]]) -> Optional[_BEnumValue]:
        """Convert an enum member or its raw value to a Bitrix24 value."""

        if value is None:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, self._enum_class):
            value = self._enum_class(value)

        return cast(_BEnumValue, value.value)
