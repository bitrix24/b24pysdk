from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Optional, Text, Type, Union

from ..._config import Config
from ..._constants import MISSING
from ...utils.type_vars import BOT
from ...utils.types import ObjectDiscriminator
from .._object_results import BitrixObjectList
from ..errors import BitrixObjectFieldError
from .base_cached_field import BaseCachedField
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "ObjectField",
]


class ObjectField(BaseCachedField[Any, BOT], Generic[BOT]):
    """Field that exposes a related Bitrix24 object through a source field.

    ``source_field`` is the real SDK field that stores the related object's primary
    key. It can be passed directly as a ``BaseField`` instance.

    ``object_class`` can be either a concrete SDK object class or its registered
    object key. String references are resolved lazily with the explicitly
    provided ``discriminator`` and then cached on the field descriptor.
    A concrete class is validated when the field is created and is not resolved
    through the registry.
    """

    __slots__ = ("_discriminator", "_object_class", "source_field")

    _discriminator: ObjectDiscriminator
    _object_class: Union[Text, Type[BOT]]
    source_field: BaseField[Any, Any]

    def __init__(
            self,
            source_field: BaseField[Any, Any],
            *,
            object_class: Union[Text, Type[BOT]],
            discriminator: ObjectDiscriminator = None,
    ):
        if isinstance(source_field, ObjectField):
            raise TypeError("ObjectField source cannot be another ObjectField.")

        if isinstance(object_class, str):
            if not object_class:
                raise ValueError("Object class key must be a non-empty string.")
        else:
            self._validate_object_class(object_class)

        super().__init__(
            bitrix_code=source_field.bitrix_code,
            is_required=source_field.is_required,
            is_read_only=source_field.is_read_only,
            is_multiple=source_field.is_multiple,
            is_pk=source_field.is_pk,
            is_updatable=source_field.is_updatable,
            request_name=source_field.request_name,
        )

        self.source_field = source_field
        self._object_class = object_class
        self._discriminator = discriminator

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
            """Return the descriptor or the cached related-object projection.

            The first instance read obtains the raw source value and converts
            primary keys into lightweight related objects. It does not fetch
            those related objects from Bitrix24. The projection is cached on the
            parent instance; ``select_related()`` later replaces its placeholders
            through this same cache.
            """

            if instance is None:
                return self

            cached_value = self.get_cached_value(instance)

            if cached_value is not MISSING:
                return cached_value

            converted_value = self.from_bitrix_value(
                instance.get_field_value(
                    self.bitrix_code,
                    bitrix_field=self.source_field,
                ),
                instance=instance,
            )

            self.set_cached_value(instance, converted_value)

            return converted_value

    def __set__(
            self,
            instance: Optional["BaseObject"],
            value: Optional[Union[BOT, Iterable[BOT]]],
    ):
        """Store related objects as both raw keys and a converted cache.

        A multiple iterable is materialized once into ``BitrixObjectList`` so
        generators are not consumed separately by raw conversion and caching.
        ``to_bitrix_value()`` validates object types and stores their primary
        keys through the source field's conversion rules. Non-``None`` objects
        are then cached directly, preserving identity for subsequent reads.
        """

        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be set on the object class.")

        self.check_is_updatable()

        if self.is_multiple and value is not None:
            if not self.is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            value = BitrixObjectList(value, client_provider=getattr(instance, "_client_provider"))

        instance.set_field_value(
            self.bitrix_code,
            self.to_bitrix_value(value),
            bitrix_field=self.source_field,
        )

        if value is None:
            self.delete_cached_value(instance)
        else:
            self.set_cached_value(instance, value)

    def __delete__(self, instance: Optional["BaseObject"]):
        self.source_field.__delete__(instance)

    @property
    def object_class(self) -> Type[BOT]:
        """Return the related SDK object class.

        String references are resolved lazily with the configured discriminator
        and then cached on the field descriptor.
        """

        object_class = self._object_class

        if not isinstance(object_class, str):
            return object_class

        try:
            resolved_object_class = Config.get_object_class(object_key=object_class, discriminator=self._discriminator)
        except KeyError:
            field_name = getattr(self, "attr_name", self.bitrix_code)
            raise BitrixObjectFieldError(
                f"No related object class is registered for "
                f"ObjectField {field_name!r} with "
                f"object_key={object_class!r} and "
                f"discriminator={self._discriminator!r}. Import or register "
                "the related object class before accessing this field.",
            ) from None

        self._validate_object_class(resolved_object_class)
        self._object_class = resolved_object_class

        return resolved_object_class

    @staticmethod
    def _validate_object_class(object_class: Type[BOT], /):
        """Validate a concrete related SDK object class once."""

        from .._base_object import BaseObject  # noqa: PLC0415

        if not (isinstance(object_class, type) and issubclass(object_class, BaseObject)):
            raise TypeError(
                f"Object class reference {object_class!r} must be "
                "a BaseObject subclass or a registered object key.",
            )

    def from_bitrix_value(
            self,
            value: Union[Optional[Any], List[Any]],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Union[Optional[BOT], BitrixObjectList[BOT]]:
        """Convert relation keys into lazy SDK object references.

        No related-object API request is performed. Multiple values are
        materialized into a ``BitrixObjectList`` and retain source order and
        duplicate keys. The owning instance's client provider is propagated to
        every placeholder and to the list so later loads use the same portal.

        As with ``BaseField``, a whole ``None`` value is permitted only for a
        non-required field, while ``None`` items inside a multiple relation are
        always rejected.
        """

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self.is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            def iter_bitrix_objects():
                for bitrix_pk in value:
                    if bitrix_pk is None:
                        raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                    bitrix_object = self._convert_from_bitrix(bitrix_pk, instance=instance)

                    if bitrix_object is not None:
                        yield bitrix_object

            return BitrixObjectList(iter_bitrix_objects(), client_provider=getattr(instance, "_client_provider"))

        return self._convert_from_bitrix(value, instance=instance)

    def _convert_from_bitrix(
            self,
            value: Optional[Any],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Optional[BOT]:
        """Convert one source value into a primary-key-only related object.

        The source descriptor performs the scalar conversion first. A non-null
        key creates a lazy object sharing the parent instance's client provider;
        none of the related object's remote fields are loaded here.
        """

        source_value = self.source_field._convert_from_bitrix(value)

        if source_value is None:
            return None

        return self.object_class(source_value, client_provider=getattr(instance, "_client_provider"))

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
