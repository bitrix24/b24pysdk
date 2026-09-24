from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Optional, Text, Union

from ..utils.type_vars import BRawT, BValueT
from ._fields import ListField
from .errors import BitrixObjectFieldError

if TYPE_CHECKING:
    from ._base_object import BaseObject
    from ._fields.base_field import BaseField

__all__ = [
    "FieldAccessor",
]


class FieldAccessor(Generic[BRawT, BValueT]):
    """Accessor for a concrete field of a concrete Bitrix24 object.

    The field descriptor keeps SDK metadata and conversion logic, while this
    accessor is bound to an object instance and exposes raw and converted
    values. ``reset()`` discards the bound field's local unsaved change through
    the owning object.
    """

    __slots__ = ("_field", "_instance")

    _instance: "BaseObject"
    _field: "BaseField[BRawT, BValueT]"

    def __init__(self, instance: "BaseObject", field: "BaseField[BRawT, BValueT]"):
        self._instance = instance
        self._field = field

    def __repr__(self) -> Text:
        return f"<{self.__class__.__name__} {self._field.attr_name!r} -> {self._field.bitrix_code!r}>"

    @property
    def raw_value(self) -> Union[Optional[BRawT], List[BRawT]]:
        """Return the raw Bitrix24 field value."""
        return self._instance.get_field_value(self._field.bitrix_code, bitrix_field=self._field)

    @raw_value.setter
    def raw_value(self, value: Union[Optional[BRawT], Iterable[BRawT]]):
        if self._field.is_multiple and value is not None:
            if not self._field.is_iterable(value):
                raise TypeError(f"Field {self._field.attr_name!r} expects an iterable raw value.")

            if not isinstance(value, list):
                value = list(value)

        self._instance.set_field_value(self._field.bitrix_code, value, bitrix_field=self._field)

    @raw_value.deleter
    def raw_value(self):
        self.reset()

    @property
    def value(self) -> Union[Optional[BValueT], List[BValueT]]:
        """Return the public Python field value."""
        return getattr(self._instance, self._field.attr_name)

    @value.setter
    def value(self, value: Union[Optional[BValueT], Iterable[BValueT]]):
        setattr(self._instance, self._field.attr_name, value)

    @value.deleter
    def value(self):
        self.reset()

    def reset(self):
        """Discard this field's local unsaved change without an API request."""
        self._instance.delete_field_value(self._field.bitrix_code, bitrix_field=self._field)

    @property
    def meta(self) -> Any:
        """Return portal-specific metadata for the bound Bitrix24 field.

        Resolution is delegated to the object so entity subclasses can override
        ``get_field()`` for special field families such as user fields. The
        object's normal per-client metadata cache rules therefore still apply.
        """
        return self._instance.get_field(self._field.bitrix_code)

    @property
    def title(self) -> Text:
        """Return the display title of the bound field.

        Resolution is delegated to the owning object because Bitrix24 APIs use
        entity-specific field metadata formats. The object's normal metadata
        cache rules apply.
        """
        return self._instance.get_field_title(self._field.bitrix_code)

    @property
    def items(self) -> List[Any]:
        """Return portal-specific choices for the bound ``ListField``.

        Checking the SDK descriptor type here prevents metadata APIs from being
        queried for scalar fields. Actual item retrieval is delegated to the
        object because standard fields and user fields may use different
        Bitrix24 endpoints and caches.

        Raises:
            BitrixObjectFieldError: If the bound descriptor is not a
                ``ListField``.
        """

        if not isinstance(self._field, ListField):
            raise BitrixObjectFieldError(
                f"Field {self._field.attr_name!r} on {self._instance.__class__.__name__} "
                "is not a ListField and has no selectable items.",
            )

        return self._instance.get_field_items(self._field.bitrix_code)

    @property
    def display_value(self) -> Any:
        """Map the current list item ID or IDs to their display values.

        Selectable items are expected to expose ``bitrix_id`` and ``value``
        attributes. Multiple field values preserve their source order and
        multiplicity. Choice collections are normally small, so this method uses
        a direct scan instead of allocating a temporary index on every access.
        An unset value or an empty multiple value returns immediately without
        loading field metadata.

        Returns:
            ``None`` for an unset field, one display value for a scalar field,
            or a list of display values for a multiple field.

        Raises:
            BitrixObjectFieldError: If an item lacks a required attribute or no
                item matches a selected ID.
        """

        field_value = self.value

        if field_value is None:
            return None

        if self._field.is_multiple and not field_value:
            return []

        items = self.items
        bitrix_ids = field_value if self._field.is_multiple else (field_value,)
        display_values = []

        # A linear scan avoids a second collection whose setup would dominate
        # the usual small list of choices.
        for bitrix_id in bitrix_ids:
            for item in items:
                try:
                    item_bitrix_id = item.bitrix_id
                except AttributeError:
                    raise BitrixObjectFieldError(
                        f"Selectable item for field {self._field.attr_name!r} "
                        "has no 'bitrix_id' attribute.",
                    ) from None

                if item_bitrix_id != bitrix_id:
                    continue

                try:
                    display_values.append(item.value)
                except AttributeError:
                    raise BitrixObjectFieldError(
                        f"Selectable item for field {self._field.attr_name!r} "
                        "has no 'value' attribute.",
                    ) from None

                break
            else:
                raise BitrixObjectFieldError(
                    f"Field {self._field.attr_name!r} has no selectable item "
                    f"with bitrix_id={bitrix_id!r}.",
                )

        return display_values if self._field.is_multiple else display_values[0]

    @display_value.setter
    def display_value(self, display_value: Union[Optional[Text], Iterable[Text]]):
        """Resolve display values to item IDs and assign the public field value.

        ``None`` clears the field. Multiple values must be a non-string iterable
        and retain their input order and duplicates. When duplicate selectable
        labels exist, the first matching item is used. Assignment goes through
        the descriptor, so ordinary conversion, read-only validation, cache
        invalidation, and local change tracking remain in effect. Empty values
        and invalid multiple-field inputs are handled before field metadata is
        requested.

        Raises:
            TypeError: If a multiple field receives a scalar display value.
            BitrixObjectFieldError: If an item lacks a required attribute or no
                item matches a requested display value.
        """

        if display_value is None:
            self.value = None
            return

        if self._field.is_multiple:
            if not self._field.is_iterable(display_value):
                raise TypeError(f"Field {self._field.attr_name!r} expects an iterable display value.")

            display_values = list(display_value)

            if not display_values:
                self.value = []
                return
        else:
            display_values = (display_value,)

        items = self.items
        bitrix_ids = []

        for selected_display_value in display_values:
            for item in items:
                try:
                    item_display_value = item.value
                except AttributeError:
                    raise BitrixObjectFieldError(
                        f"Selectable item for field {self._field.attr_name!r} "
                        "has no 'value' attribute.",
                    ) from None

                if item_display_value != selected_display_value:
                    continue

                try:
                    bitrix_ids.append(item.bitrix_id)
                except AttributeError:
                    raise BitrixObjectFieldError(
                        f"Selectable item for field {self._field.attr_name!r} "
                        "has no 'bitrix_id' attribute.",
                    ) from None

                break
            else:
                raise BitrixObjectFieldError(
                    f"Field {self._field.attr_name!r} has no selectable item "
                    f"with value={selected_display_value!r}.",
                )

        self.value = bitrix_ids if self._field.is_multiple else bitrix_ids[0]
