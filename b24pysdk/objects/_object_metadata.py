from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, Dict, Hashable, List, Mapping, Optional, Text, Tuple, Type

from ..utils.types import cast
from .errors import BitrixObjectError, BitrixObjectFieldError
from .fields.base_field import BaseField

if TYPE_CHECKING:
    from ._base_object import BaseObject

__all__ = [
    "ObjectMetadata",
]


class ObjectMetadata:
    """Immutable field metadata for an SDK object class."""

    __slots__ = (
        "_fields_by_attr_name",
        "_fields_by_bitrix_code",
        "_pk_fields",
        "object_class",
        "pk_type",
    )

    object_class: Type["BaseObject[Any]"]
    pk_type: Type[Hashable]

    _fields_by_attr_name: Mapping[Text, BaseField[Any, Any]]
    _fields_by_bitrix_code: Mapping[Text, BaseField[Any, Any]]
    _pk_fields: Tuple[BaseField[Any, Any], ...]

    def __init__(self, object_class: Type["BaseObject[Any]"], /):
        self.object_class = object_class

        try:
            pk_type = getattr(object_class, "_PK_TYPE")
        except AttributeError:
            raise BitrixObjectError(
                f"{object_class.__name__} must define the _PK_TYPE class attribute.",
            ) from None

        if not isinstance(pk_type, type):
            raise BitrixObjectError(
                f"{object_class.__name__}._PK_TYPE must be a type, "
                f"got {type(pk_type).__name__!r}.",
            )

        if not issubclass(pk_type, Hashable):
            raise BitrixObjectError(
                f"{object_class.__name__}._PK_TYPE must define a hashable "
                "primary-key type.",
            )

        self.pk_type = pk_type

        fields_by_attr_name: Dict[Text, BaseField[Any, Any]] = {}
        fields_by_bitrix_code: Dict[Text, BaseField[Any, Any]] = {}

        for base_class in reversed(cast(Tuple[Type], object_class.__mro__)):
            local_fields_by_bitrix_code: Dict[Text, BaseField[Any, Any]] = {}

            for attr_name, field in base_class.__dict__.items():
                if not isinstance(field, BaseField):
                    continue

                fields_by_attr_name[attr_name] = field
                source_field = getattr(field, "_source_field", None)

                if isinstance(source_field, BaseField):
                    if source_field.bitrix_code not in fields_by_bitrix_code:
                        raise BitrixObjectFieldError(
                            f"Object field {attr_name!r} uses unregistered source field "
                            f"{source_field.bitrix_code!r} on {base_class.__name__}.",
                        )

                    continue

                existing_local_field = local_fields_by_bitrix_code.get(field.bitrix_code)

                if existing_local_field is not None and existing_local_field is not field:
                    raise BitrixObjectFieldError(
                        f"Bitrix field {field.bitrix_code!r} is declared more than once "
                        f"on {base_class.__name__}.",
                    )

                local_fields_by_bitrix_code[field.bitrix_code] = field

                fields_by_bitrix_code[field.bitrix_code] = field

        pk_fields: List[BaseField[Any, Any]] = [
            field
            for field in fields_by_bitrix_code.values()
            if field.is_pk
        ]

        self._fields_by_attr_name = MappingProxyType(fields_by_attr_name)
        self._fields_by_bitrix_code = MappingProxyType(fields_by_bitrix_code)
        self._pk_fields = tuple(pk_fields)

    def __repr__(self) -> Text:
        return f"<{self.__class__.__name__} object_class={self.object_class.__name__!r}>"

    @property
    def fields_by_bitrix_code(self) -> Mapping[Text, BaseField[Any, Any]]:
        """Return concrete fields indexed by Bitrix24 field code."""
        return self._fields_by_bitrix_code

    @property
    def pk_fields(self) -> Tuple[BaseField[Any, Any], ...]:
        """Return fields that form the object primary key."""
        return self._pk_fields

    @property
    def pk_field(self) -> Optional[BaseField[Any, Any]]:
        """Return the single primary-key field or None for a composite key."""

        if len(self._pk_fields) != 1:
            return None

        return self._pk_fields[0]

    def build_bitrix_pk(self, *values: Any) -> Hashable:
        """Build the public primary-key value from raw Bitrix24 values."""

        if not values:
            raise ValueError("Pass at least one primary-key value.")

        if len(values) == 1 and isinstance(values[0], self.pk_type):
            return values[0]

        pk_factory = cast(Callable[..., Hashable], self.pk_type)
        return pk_factory(*values)

    def get_field(self, attr_name: Text) -> BaseField[Any, Any]:
        """Return a field by SDK object attribute name."""

        try:
            return self._fields_by_attr_name[attr_name]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no field attribute {attr_name!r}.",
            ) from None

    def get_field_by_bitrix_code(self, bitrix_code: Text) -> BaseField[Any, Any]:
        """Return a concrete field by Bitrix24 field code."""

        try:
            return self._fields_by_bitrix_code[bitrix_code]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no registered "
                f"Bitrix field {bitrix_code!r}.",
            ) from None
