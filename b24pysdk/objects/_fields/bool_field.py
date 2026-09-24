from typing import TYPE_CHECKING, List, Optional, Text, Type, Union

from ...utils.converters import bool_from_bitrix, bool_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "BoolField",
]


class BoolField(BaseField[Union[bool, int, Text], bool]):
    """Field that exposes a Bitrix24 boolean-like value as ``bool``.

    Incoming values are accepted in every boolean format used by Bitrix24:
    ``True``/``False``, ``1``/``0``, and ``Y``/``N``. ``serialize_as`` controls
    only the outgoing representation and defaults to the legacy ``Y``/``N``
    format. Pass ``int`` for ``1``/``0`` or ``bool`` for API v3 booleans.
    """

    __slots__ = ("_serialize_as",)

    _serialize_as: Type[Union[bool, int, Text]]

    def __init__(
            self,
            bitrix_code: Text,
            *,
            serialize_as: Type[Union[bool, int, Text]] = str,
            is_pk: bool = False,
            is_required: Optional[bool] = None,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_updatable: bool = True,
            request_name: Optional[Text] = None,
    ):
        if serialize_as not in (bool, int, str):
            raise TypeError("serialize_as must be bool, int, or str.")

        super().__init__(
            bitrix_code=bitrix_code,
            is_pk=is_pk,
            is_required=is_required,
            is_multiple=is_multiple,
            is_read_only=is_read_only,
            is_updatable=is_updatable,
            request_name=request_name,
        )
        self._serialize_as = serialize_as

    @property
    def serialize_as(self) -> Type[Union[bool, int, Text]]:
        """Return the immutable type used to serialize outgoing values."""
        return self._serialize_as

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

    def _convert_to_bitrix(self, value: Optional[bool]) -> Optional[Union[bool, int, Text]]:
        """Convert a single Python ``bool`` value to a Bitrix24 boolean value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return bool_to_bitrix(value, is_required=True, serialize_as=self._serialize_as)

        return bool_to_bitrix(value, is_required=False, serialize_as=self._serialize_as)
