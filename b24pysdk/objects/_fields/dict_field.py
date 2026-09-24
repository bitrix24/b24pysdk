from typing import TYPE_CHECKING, List, Literal, NoReturn, Optional, Type, Union

from ...utils.converters import dict_from_bitrix, dict_to_bitrix
from ...utils.types import JSONDict, cast
from .._filter_lookups import NO_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "DictField",
]


class DictField(BaseField[Union[JSONDict, List[NoReturn], Literal[False]], JSONDict]):
    """Field that exposes a Bitrix24 dictionary value as ``dict``.

    Some Bitrix24 methods serialize an absent dictionary as ``false`` and an
    empty associative array as ``[]`` instead of ``{}``. ``False`` is
    normalized to ``None`` and an empty list to an empty dictionary. Non-empty
    lists remain invalid.

    Loaded mappings preserve their object identity. An in-place change can
    therefore be persisted explicitly with ``save(update_fields=[...])``. It
    does not create a local assignment and is not included in a parameterless
    ``save()`` call.
    """

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["DictField", Optional[JSONDict], List[NoReturn]]: ...

    def _convert_from_bitrix(self, value: Optional[Union[JSONDict, List[NoReturn], Literal[False]]]) -> Optional[JSONDict]:
        """Convert a raw mapping, empty array, or false value to Python."""

        if value is False:
            value = None

        if isinstance(value, list):
            if value:
                raise ValueError(f"Cannot convert non-empty Bitrix24 list to dict: {value!r}")

            value = {}

        value = cast(Optional[JSONDict], value)

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
