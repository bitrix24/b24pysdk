import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Iterable, List, Mapping, Optional, Text, Type, Union

from ...utils.type_vars import BRawT, BValueT
from ...utils.types import Self
from .._filter_lookups import BASIC_FILTER_OPERATORS, BaseFilterOperator, FilterLookup
from ..errors import BitrixObjectFieldReadOnlyError, BitrixObjectFilterError

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

    ``request_name`` may be supplied explicitly when an API wrapper uses a
    parameter name that cannot be derived from the Bitrix24 field code.
    Otherwise, it is generated from ``bitrix_code`` in ``snake_case``. The
    special primary-key codes ``ID`` and ``id`` are mapped to ``bitrix_id``.

    If ``is_pk=True`` is set, the field is treated as required by default and
    read-only automatically. A nullable component of a composite key may opt
    out explicitly with ``is_required=False``. Read-only fields are also never
    updatable. Setting ``is_updatable=False`` without making a field read-only
    creates an add-only field: managers may pass it during object creation, but
    existing objects and manager queries cannot update it.

    When complete Bitrix24 object data omits a non-required field, the object
    treats that field as raw ``None``. Missing fields in partial responses are
    resolved by loading complete object data first.

    Required and multiple flags affect the public value as follows:

    * single, not required: ``Optional[BValueT]``;
    * single, required: ``BValueT``;
    * multiple, not required: ``Optional[List[BValueT]]``;
    * multiple, required: ``List[BValueT]``.

    For multiple fields, ``None`` is allowed only as the whole field value when
    the field is not required. ``None`` items inside a multiple-value list are
    not allowed. An empty list is a valid value even for required multiple
    fields.

    ``_FILTER_OPERATORS`` maps explicit lookup names to their operator implementations for
    this field type. Plain equality is always available and is not registered as
    a lookup.
    """

    __slots__ = (
        "attr_name",
        "bitrix_code",
        "is_multiple",
        "is_pk",
        "is_read_only",
        "is_required",
        "is_updatable",
        "request_name",
    )
    attr_name: Text
    bitrix_code: Text
    is_multiple: bool
    is_pk: bool
    is_read_only: bool
    is_required: bool
    is_updatable: bool
    request_name: Text

    _FILTER_OPERATORS: ClassVar[Mapping[FilterLookup, Type[BaseFilterOperator]]] = BASIC_FILTER_OPERATORS

    def __init__(
            self,
            bitrix_code: Text,
            *,
            is_pk: bool = False,
            is_required: Optional[bool] = None,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_updatable: bool = True,
            request_name: Optional[Text] = None,
    ):
        effective_is_required = is_pk if is_required is None else is_required

        self.bitrix_code = bitrix_code
        self.is_pk = is_pk
        self.is_required = effective_is_required
        self.is_multiple = is_multiple
        self.is_read_only = is_read_only or is_pk
        self.is_updatable = is_updatable and not self.is_read_only
        self.request_name = self._get_request_name(bitrix_code) if request_name is None else request_name

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
        """Return the descriptor on a class or a converted value on an object.

        Instance access asks the object for the raw value, allowing local data,
        lazy loading, and primary-key handling to remain centralized in
        ``BaseObject``. Primary-key values are already normalized when the key
        is constructed and are returned directly. Other values are converted
        on every read; cached field subclasses override this behavior when
        conversion creates richer objects.
        """

        if instance is None:
            return self

        value = instance.get_field_value(self.bitrix_code, bitrix_field=self)

        if self.is_pk:
            return value

        return self.from_bitrix_value(value)

    def __set__(
            self,
            instance: Optional["BaseObject"],
            value: Union[Optional[BValueT], Iterable[BValueT]],
    ):
        """Convert and store a public value as an unsaved raw field value.

        No remote request is made. ``BaseObject.set_field_value()`` records the
        converted value in local state and invalidates cached projections backed
        by the same Bitrix24 code.
        """

        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be set on the object class.")

        self.check_is_updatable()

        instance.set_field_value(self.bitrix_code, self.to_bitrix_value(value), bitrix_field=self)

    def __delete__(self, instance: Optional["BaseObject"]):
        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be deleted from the object class.")

        instance.delete_field_value(self.bitrix_code, bitrix_field=self)

    def check_is_updatable(self):
        """Raise when this field cannot be changed on an existing object.

        Read-only fields cannot participate in either creation or updates.
        Non-updatable fields may still be supplied when an object is created,
        but become immutable afterward.
        """

        if self.is_updatable:
            return

        if self.is_read_only:
            raise BitrixObjectFieldReadOnlyError(f"Field {self.attr_name!r} is read-only.")

        raise BitrixObjectFieldReadOnlyError(
            f"Field {self.attr_name!r} cannot be updated after object creation.",
        )

    @staticmethod
    def _get_request_name(bitrix_code: Text) -> Text:
        """Convert a Bitrix24 field code to a Python API wrapper parameter name."""

        if bitrix_code.lower() == "id":
            return "bitrix_id"

        request_name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", bitrix_code)
        request_name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", request_name)

        return request_name.lower()

    @staticmethod
    def is_iterable(value: Any) -> bool:
        """Return whether a value is a supported multiple-field container.

        Strings and byte sequences are scalar field values even though Python
        considers them iterable. Dictionaries are rejected because iterating
        their keys is almost never the caller's intent. General iterables,
        including generators, are accepted and consumed once by conversion.
        """

        if isinstance(value, (Mapping, bytes, bytearray, str)) or value is None:
            return False

        return isinstance(value, Iterable)

    def get_filter_operator(self, lookup: FilterLookup, /) -> Type[BaseFilterOperator]:
        """Return the filter operator implementation supported by this field type."""
        try:
            return self._FILTER_OPERATORS[lookup]
        except KeyError:
            raise BitrixObjectFilterError(
                f"Field {self.attr_name!r} ({self.__class__.__name__}) does not support "
                f"filter lookup {lookup.value!r}.",
            ) from None

    def from_bitrix_value(self, value: Union[Optional[BRawT], List[BRawT]]) -> Union[Optional[BValueT], List[BValueT]]:
        """Convert a raw Bitrix24 field value to its public representation.

        Multiple fields accept any supported iterable and eagerly return a new
        list, ensuring one-pass API iterables do not leak into object state.
        ``None`` may represent the whole field only when it is not required;
        individual ``None`` items are always rejected. Empty iterables remain
        valid. Scalar conversion is delegated directly to the concrete field so
        it can enforce its own empty-value semantics.
        """

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self.is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            converted_values = []

            for item in value:
                if item is None:
                    raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                converted_value = self._convert_from_bitrix(item)

                if converted_value is not None:
                    converted_values.append(converted_value)

            return converted_values

        return self._convert_from_bitrix(value)

    def to_bitrix_value(self, value: Union[Optional[BValueT], Iterable[BValueT]]) -> Union[Optional[BRawT], List[BRawT]]:
        """Convert a public field value to its raw Bitrix24 representation.

        Multiple inputs are validated and consumed eagerly into a new list.
        Appending, removing, or reordering items in the caller's container then
        cannot change the converted container, and generators have deterministic
        one-pass behavior. Whole-value and per-item ``None`` rules mirror
        ``from_bitrix_value()``. Scalar conversion is delegated to the concrete
        field implementation.
        """

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self.is_iterable(value):
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
