import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Optional, Text, Type, Union

from ...utils.type_vars import BRawT, BValueT
from ...utils.types import Self
from ..errors import BitrixObjectFieldReadOnlyError

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "BaseField",
]


class BaseField(ABC, Generic[BRawT, BValueT]):
    """Base descriptor that maps a Python object attribute to a Bitrix24 field.

    ``BaseField`` stores field metadata and implements descriptor behavior. The
    owning object stores raw values by Bitrix24 field code, while the descriptor
    converts values between the raw Bitrix24 representation and the public
    Python representation.

    Access through the object class returns the field descriptor::

        Deal.title

    Access through an object instance returns the converted Python value::

        deal.title

    Assignment through an object instance converts the Python value back to raw
    Bitrix24 form and stores it in the object's local changed-data storage::

        deal.title = "New title"

    ``request_name`` is generated from ``bitrix_code`` in ``snake_case``.
    The special Bitrix24 primary-key codes ``ID`` and ``id`` are mapped to
    ``bitrix_id``.

    If ``is_pk=True`` is set, the field is treated as required and read-only
    automatically.

    If Bitrix24 may omit an optional field from the response, set
    ``is_missing_allowed=True``. In that case a missing registered field is
    treated as raw ``None`` instead of a field-loading error.

    Required and multiple flags affect the public value as follows:

    * single, not required: ``Optional[BValueT]``;
    * single, required: ``BValueT``;
    * multiple, not required: ``Optional[List[BValueT]]``;
    * multiple, required: ``List[BValueT]``.

    For multiple fields, ``None`` is allowed only as the whole field value when
    the field is not required. ``None`` items inside a multiple-value list are
    not allowed. An empty list is a valid value even for required multiple
    fields.
    """

    __slots__ = (
        "attr_name",
        "bitrix_code",
        "is_missing_allowed",
        "is_multiple",
        "is_pk",
        "is_read_only",
        "is_required",
        "request_name",
    )
    attr_name: Text
    bitrix_code: Text
    is_missing_allowed: bool
    is_multiple: bool
    is_pk: bool
    is_read_only: bool
    is_required: bool
    request_name: Text

    def __init__(
            self,
            bitrix_code: Text,
            *,
            is_pk: bool = False,
            is_required: bool = False,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_missing_allowed: bool = False,
    ):
        effective_is_required = is_required or is_pk

        if effective_is_required and is_missing_allowed:
            raise ValueError("Required field cannot allow missing Bitrix24 value.")

        self.bitrix_code = bitrix_code
        self.is_pk = is_pk
        self.is_required = effective_is_required
        self.is_multiple = is_multiple
        self.is_read_only = is_read_only or is_pk
        self.is_missing_allowed = is_missing_allowed
        self.request_name = self._get_request_name(bitrix_code)

    def __repr__(self) -> Text:
        if hasattr(self, "attr_name"):
            return f"<{self.__class__.__name__} {self.attr_name!r} -> {self.bitrix_code!r}>"
        else:
            return f"<{self.__class__.__name__} -> {self.bitrix_code!r}>"

    def __eq__(self, other: "BaseField") -> bool:
        return isinstance(other, BaseField) and self.bitrix_code == other.bitrix_code

    def __hash__(self) -> int:
        return hash(self.bitrix_code)

    def __set_name__(self, owner: Type["BaseObject"], name: Text):
        self.attr_name = name

    def __get__(
            self,
            instance: Optional["BaseObject"],
            owner: Type["BaseObject"],
    ) -> Union[Self, Optional[BValueT], List[BValueT]]:
        if instance is None:
            return self

        return self.from_bitrix_value(instance[self.bitrix_code])

    def __set__(self, instance: Optional["BaseObject"], value: Union[Optional[BValueT], List[BValueT]]):
        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be set on the object class.")

        if self.is_read_only:
            raise BitrixObjectFieldReadOnlyError(f"Field {self.attr_name!r} is read-only.")

        instance[self.bitrix_code] = self.to_bitrix_value(value)
        self.delete_private_attr(instance)

    def __delete__(self, instance: Optional["BaseObject"]):
        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be deleted from the object class.")

        del instance[self.bitrix_code]
        self.delete_private_attr(instance)

    @staticmethod
    def _get_request_name(bitrix_code: Text) -> Text:
        """Convert a Bitrix24 field code to a Python API wrapper parameter name."""

        if bitrix_code.lower() == "id":
            return "bitrix_id"

        request_name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", bitrix_code)
        request_name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", request_name)

        return request_name.lower()

    @staticmethod
    def _is_iterable(value: Any) -> bool:
        """Return whether a value can be treated as a multiple field container."""

        if isinstance(value, (str, bytes, bytearray, dict)) or value is None:
            return False

        return isinstance(value, Iterable)

    def get_private_attr_name(self, owner: Type["BaseObject"]) -> Text:
        """Return a private instance attribute name reserved for this field."""
        return f"_{owner.__name__}__{self.attr_name}"

    def delete_private_attr(self, instance: "BaseObject"):
        """Delete this field private instance attribute, if it exists."""
        instance.__dict__.pop(self.get_private_attr_name(instance.__class__), None)

    def from_bitrix_value(self, value: Union[Optional[BRawT], List[BRawT]]) -> Union[Optional[BValueT], List[BValueT]]:
        """Convert a raw Bitrix24 field value to a public Python value."""

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self._is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            converted_values = []

            for item in value:
                if item is None:
                    raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                converted_values.append(self._convert_from_bitrix(item))

            return converted_values

        return self._convert_from_bitrix(value)

    def to_bitrix_value(self, value: Union[Optional[BValueT], List[BValueT]]) -> Union[Optional[BRawT], List[BRawT]]:
        """Convert a public Python field value to a raw Bitrix24 value."""

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self._is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            converted_values = []

            for item in value:
                if item is None:
                    raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                converted_values.append(self._convert_to_bitrix(item))

            return converted_values

        return self._convert_to_bitrix(value)

    @abstractmethod
    def _convert_from_bitrix(self, value: Optional[BRawT]) -> Optional[BValueT]:
        """Convert a single raw Bitrix24 value to a public Python value."""
        raise NotImplementedError

    @abstractmethod
    def _convert_to_bitrix(self, value: Optional[BValueT]) -> Optional[BRawT]:
        """Convert a single public Python value to a raw Bitrix24 value."""
        raise NotImplementedError
