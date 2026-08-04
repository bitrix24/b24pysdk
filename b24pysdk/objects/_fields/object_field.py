from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Optional, Text, Type, Union

from ..._config import Config
from ..._constants import MISSING
from ...utils.type_vars import BOT
from .._bitrix_object_list import BitrixObjectList
from ..errors import BitrixObjectFieldReadOnlyError
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "ObjectField",
]


class ObjectField(BaseField[Any, BOT], Generic[BOT]):
    """Field that exposes a related Bitrix24 object through a source field.

    ``source_field`` is the real SDK field that stores the related object's primary
    key. It can be passed directly as a ``BaseField`` instance.

    ``object_class`` can be either a concrete SDK object class or its registered
    object key. Object keys are resolved lazily through ``Config`` to avoid cyclic
    imports and to use the most recently registered object subclass. A concrete
    class is used directly and is not resolved again through the registry.

    ``request_name`` belongs to the object field itself. If omitted, it defaults
    to this descriptor's attribute name rather than the source field name.
    """

    __slots__ = ("_object_class", "source_field")

    _object_class: Union[Text, Type[BOT]]
    source_field: BaseField[Any, Any]

    def __init__(
            self,
            source_field: BaseField[Any, Any],
            *,
            object_class: Union[Text, Type[BOT]],
    ):
        if isinstance(source_field, ObjectField):
            raise TypeError("ObjectField source cannot be another ObjectField.")

        super().__init__(
            bitrix_code=source_field.bitrix_code,
            is_required=source_field.is_required,
            is_read_only=source_field.is_read_only,
            is_multiple=source_field.is_multiple,
            is_pk=source_field.is_pk,
            is_missing_allowed=source_field.is_missing_allowed,
        )

        self.source_field = source_field
        self._object_class = object_class

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["ObjectField[BOT]", Optional[BOT], BitrixObjectList[BOT]]: ...
    else:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["ObjectField[BOT]", Optional[BOT], BitrixObjectList[BOT]]:
            if instance is None:
                return self

            cached_value = self._get_cached_value(instance)

            if cached_value is not None:
                return cached_value

            converted_value = self.from_bitrix_value(instance[self.bitrix_code], instance=instance)

            if converted_value is not None:
                self._set_cached_value(instance, converted_value)

            return converted_value

    def __set__(
            self,
            instance: Optional["BaseObject"],
            value: Optional[Union[BOT, Iterable[BOT]]],
    ):
        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be set on the object class.")

        if self.is_read_only:
            raise BitrixObjectFieldReadOnlyError(f"Field {self.attr_name!r} is read-only.")

        if self.is_multiple and value is not None:
            if not self._is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            value = BitrixObjectList(value, client_provider=getattr(instance, "_client_provider"))

        instance[self.bitrix_code] = self.to_bitrix_value(value)

        if value is None:
            self._delete_cached_value(instance)
        else:
            self._set_cached_value(instance, value)

    def __delete__(self, instance: Optional["BaseObject"]):
        self.source_field.__delete__(instance)

    @property
    def object_class(self) -> Type[BOT]:
        """Return the related SDK object class."""

        object_class_reference = self._object_class

        if isinstance(object_class_reference, str):
            if not object_class_reference:
                raise ValueError("Object class key must be a non-empty string.")

            return Config.get_object_class(object_key=object_class_reference)

        from .._base_object import BaseObject  # noqa: PLC0415

        if not issubclass(object_class_reference, BaseObject):
            raise TypeError(
                f"Object class reference {object_class_reference!r} must be "
                "a BaseObject subclass or a registered object key.",
            )

        return object_class_reference

    def from_bitrix_value(
            self,
            value: Union[Optional[Any], List[Any]],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Union[Optional[BOT], BitrixObjectList[BOT]]:
        """Convert a raw Bitrix24 field value to a public Python value."""

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self._is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            def iter_bitrix_objects():
                for bitrix_pk in value:
                    if bitrix_pk is None:
                        raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                    yield self._convert_from_bitrix(bitrix_pk, instance=instance)

            return BitrixObjectList(iter_bitrix_objects(), client_provider=getattr(instance, "_client_provider"))

        return self._convert_from_bitrix(value, instance=instance)

    def _convert_from_bitrix(
            self,
            value: Optional[Any],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Optional[BOT]:
        """Convert one related primary key to an SDK object."""

        source_value = self.source_field._convert_from_bitrix(value)

        if source_value is None:
            return None

        return self.object_class(source_value, client=instance.client)

    def _convert_to_bitrix(self, value: Optional[BOT]) -> Any:
        """Convert one related SDK object to its raw primary-key value."""
        source_value = None if value is None else self._get_bitrix_pk(value)
        return self.source_field._convert_to_bitrix(source_value)

    def _get_bitrix_pk(self, bitrix_object: BOT) -> Any:
        """Return primary key from a related SDK object."""

        object_class = self.object_class

        if not isinstance(bitrix_object, object_class):
            raise TypeError(
                f"Field {self.attr_name!r} expects {object_class.__name__} object or None, "
                f"got {type(bitrix_object).__name__}.",
            )

        return bitrix_object.bitrix_pk

    def _get_cache_attr_name(self, instance: "BaseObject") -> Text:
        """Return the private attribute name used for this object-field cache."""
        return self.get_private_attr_name(instance.__class__)

    def _get_cached_value(self, instance: "BaseObject") -> Union[Optional[BOT], BitrixObjectList[BOT]]:
        """Return the cached related object for this object field."""
        return getattr(instance, self._get_cache_attr_name(instance), None)

    def _delete_cached_value(self, instance: "BaseObject"):
        """Delete the cached related object for this object field, if it exists."""
        self.delete_private_attr(instance)

    def _set_cached_value(self, instance: "BaseObject", value: Union[Optional[BOT], BitrixObjectList[BOT]]):
        """Cache a related object under this object field's private attribute."""
        setattr(instance, self._get_cache_attr_name(instance), value)
