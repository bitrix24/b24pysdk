import importlib
from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Literal, Optional, Text, Type, Union

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

    ``object_class`` can be either a concrete SDK object class, ``"self"``,
    or a dotted import path. ``"self"`` refers to the object class on which this
    field is declared. Absolute paths are imported as-is. Paths starting with a
    dot are resolved relative to the package of the declaring module. String
    references are resolved lazily to avoid cyclic imports.

    ``request_name`` belongs to the object field itself. If omitted, it defaults
    to this descriptor's attribute name rather than the source field name.
    """

    __slots__ = ("_object_class", "_owner_class", "_source_field")

    _owner_class: Type["BaseObject"]
    _source_field: BaseField[Any, Any]
    _object_class: Union[Literal["self"], Text, Type[BOT]]

    def __init__(
            self,
            source_field: BaseField[Any, Any],
            *,
            object_class: Union[Literal["self"], Text, Type[BOT]],
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

        self._source_field = source_field
        self._object_class = object_class

    def __set_name__(self, owner: Type["BaseObject"], name: Text):
        super().__set_name__(owner, name)
        self._owner_class = owner

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

            value = BitrixObjectList(value, client_provider=instance._client_provider)

        instance[self.bitrix_code] = self.to_bitrix_value(value)

        if value is None:
            self._delete_cached_value(instance)
        else:
            self._set_cached_value(instance, value)

    def __delete__(self, instance: Optional["BaseObject"]):
        self._source_field.__delete__(instance)

    @property
    def object_class(self) -> Type[BOT]:
        """Return and validate the related SDK object class."""

        object_class_reference = self._object_class

        if isinstance(object_class_reference, str):
            if object_class_reference == "self":
                try:
                    object_class = self._owner_class
                except AttributeError:
                    raise RuntimeError(
                        'Object class reference "self" can be resolved only after '
                        "ObjectField is assigned to an object class.",
                    ) from None
            else:
                try:
                    module_path, class_name = object_class_reference.rsplit(".", maxsplit=1)
                except ValueError:
                    raise ValueError(
                        f"Object class path {object_class_reference!r} must include a module and class name.",
                    ) from None

                if not module_path or not class_name:
                    raise ValueError(
                        f"Object class path {object_class_reference!r} must include a module and class name.",
                    )

                package = None

                if module_path.startswith("."):
                    try:
                        owner_module_path = self._owner_class.__module__
                    except AttributeError:
                        raise RuntimeError(
                            "Relative object class path can be resolved only after "
                            "ObjectField is assigned to an object class.",
                        ) from None

                    owner_module = importlib.import_module(owner_module_path)
                    package = owner_module.__package__

                    if not package:
                        raise ImportError(
                            f"Cannot resolve relative object class path {object_class_reference!r}: "
                            f"module {owner_module_path!r} has no package.",
                        )

                module = importlib.import_module(module_path, package=package)
                object_class = getattr(module, class_name)
        else:
            object_class = object_class_reference

        from .._base_object import BaseObject  # noqa: PLC0415

        if not isinstance(object_class, type) or not issubclass(object_class, BaseObject):
            raise TypeError(
                f"Object class reference {object_class_reference!r} must resolve "
                "to a BaseObject subclass.",
            )

        self._object_class = object_class
        return object_class

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

            bitrix_objects = []

            for bitrix_pk in value:
                if bitrix_pk is None:
                    raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                bitrix_objects.append(self._convert_from_bitrix(bitrix_pk, instance=instance))

            return BitrixObjectList(bitrix_objects, client_provider=instance._client_provider)

        return self._convert_from_bitrix(value, instance=instance)

    def _convert_from_bitrix(
            self,
            value: Optional[Any],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Optional[BOT]:
        """Convert one related primary key to an SDK object."""

        source_value = self._source_field._convert_from_bitrix(value)

        if source_value is None:
            return None

        return self.object_class(source_value, client=instance.client)

    def _convert_to_bitrix(self, value: Optional[BOT]) -> Any:
        """Convert one related SDK object to its raw primary-key value."""
        source_value = None if value is None else self._get_bitrix_pk(value)
        return self._source_field._convert_to_bitrix(source_value)

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
        """Return the source field private attribute name used for related-object cache."""
        return self._source_field.get_private_attr_name(instance.__class__)

    def _get_cached_value(self, instance: "BaseObject") -> Union[Optional[BOT], BitrixObjectList[BOT]]:
        """Return a cached related object from the source field private attribute."""
        return getattr(instance, self._get_cache_attr_name(instance), None)

    def _delete_cached_value(self, instance: "BaseObject"):
        """Delete the cached related object, if it exists."""
        self._source_field.delete_private_attr(instance)

    def _set_cached_value(self, instance: "BaseObject", value: Union[Optional[BOT], BitrixObjectList[BOT]]):
        """Cache a related object under the source field private attribute."""
        setattr(instance, self._get_cache_attr_name(instance), value)
