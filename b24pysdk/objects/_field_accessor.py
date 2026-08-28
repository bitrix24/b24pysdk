from typing import TYPE_CHECKING, Any, Generic, List, Optional, Text, Union

from ..utils.type_vars import BRawT, BValueT

if TYPE_CHECKING:
    from ._base_object import BaseObject
    from ._fields.base_field import BaseField

__all__ = [
    "FieldAccessor",
]


class FieldAccessor(Generic[BRawT, BValueT]):
    """Accessor for a concrete field of a concrete Bitrix24 object.

    The field descriptor keeps SDK metadata and conversion logic, while this
    accessor is bound to an object instance and exposes raw and converted values.
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
    def raw_value(self, value: Union[Optional[BRawT], List[BRawT]]):
        self._instance.set_field_value(self._field.bitrix_code, value, bitrix_field=self._field)

    @raw_value.deleter
    def raw_value(self):
        self._instance.delete_field_value(self._field.bitrix_code, bitrix_field=self._field)

    @property
    def value(self) -> Union[Optional[BValueT], List[BValueT]]:
        """Return the public Python field value."""
        return getattr(self._instance, self._field.attr_name)

    @value.setter
    def value(self, value: Union[Optional[BValueT], List[BValueT]]):
        setattr(self._instance, self._field.attr_name, value)

    @value.deleter
    def value(self):
        delattr(self._instance, self._field.attr_name)

    @property
    def meta(self) -> Any:
        """Return field metadata for this object field."""
        return self._instance.get_field(self._field.bitrix_code)
