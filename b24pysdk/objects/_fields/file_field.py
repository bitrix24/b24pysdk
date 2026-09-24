from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Optional, Text, Type, TypeVar, Union

from ..._constants import MISSING
from ...schemas._base_file_schema import BaseFileSchema
from .._filter_lookups import NO_FILTER_OPERATORS
from .base_cached_field import BaseCachedField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "FileField",
]


_BFileT = TypeVar("_BFileT", bound=BaseFileSchema)


class FileField(BaseCachedField[Any, _BFileT], Generic[_BFileT]):
    """Cached field that exposes a Bitrix24 file through a file schema class.

    ``file_class`` defines the concrete file representation used by this
    Bitrix24 entity. The converted ``BaseFileSchema`` subclass instance is
    cached on the owning object in the same way as an ``ObjectField`` value.
    File content caching belongs to the concrete file object itself.

    Remote file objects receive the owning object's Bitrix24 portal domain when
    they are created. File schemas that do not need it can ignore the context.
    """

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    __slots__ = ("_file_class",)

    _file_class: Type[_BFileT]

    def __init__(
            self,
            bitrix_code: Text,
            *,
            file_class: Type[_BFileT],
            is_pk: bool = False,
            is_required: Optional[bool] = None,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_updatable: bool = True,
            request_name: Optional[Text] = None,
    ):
        if not issubclass(file_class, BaseFileSchema):
            raise TypeError("file_class must be a BaseFileSchema subclass.")

        super().__init__(
            bitrix_code=bitrix_code,
            is_pk=is_pk,
            is_required=is_required,
            is_multiple=is_multiple,
            is_read_only=is_read_only,
            is_updatable=is_updatable,
            request_name=request_name,
        )
        self._file_class = file_class

    @property
    def file_class(self) -> Type[_BFileT]:
        """Return the immutable file schema class used by this field."""
        return self._file_class

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["FileField[_BFileT]", Optional[_BFileT], List[_BFileT]]: ...
    else:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["FileField[_BFileT]", Optional[_BFileT], List[_BFileT]]:
            """Return the descriptor or a cached converted file value.

            The first instance read converts raw field data with portal context
            from the owning object and caches the resulting file object or list.
            Later reads reuse that projection until its source Bitrix24 value is
            changed, refreshed, or successfully updated.
            """

            if instance is None:
                return self

            cached_value = self.get_cached_value(instance)

            if cached_value is not MISSING:
                return cached_value

            converted_value = self.from_bitrix_value(
                instance.get_field_value(
                    self.bitrix_code,
                    bitrix_field=self,
                ),
                instance=instance,
            )

            self.set_cached_value(instance, converted_value)

            return converted_value

    def __set__(
            self,
            instance: Optional["BaseObject"],
            value: Optional[Union[_BFileT, Iterable[_BFileT]]],
    ):
        """Store file objects as raw write data and a converted cache.

        Multiple iterables are materialized once so a generator can be converted
        and cached consistently. Raw write values are recorded as local changes;
        non-null public file objects are cached to preserve identity until the
        object is refreshed or the update is confirmed.
        """

        if instance is None:
            raise AttributeError(f"Field {self!r} cannot be set on the object class.")

        self.check_is_updatable()

        if self.is_multiple and value is not None:
            if not self.is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            value = list(value)

        instance.set_field_value(
            self.bitrix_code,
            self.to_bitrix_value(value),
            bitrix_field=self,
        )

        if value is None:
            self.delete_cached_value(instance)
        else:
            self.set_cached_value(instance, value)

    def from_bitrix_value(
            self,
            value: Union[Optional[Any], List[Any]],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Union[Optional[_BFileT], List[_BFileT]]:
        """Convert raw file metadata into portal-aware file objects.

        Multiple values are eagerly converted into a new list. The owning object
        is forwarded to scalar conversion so remote file schemas receive the
        correct portal domain. Whole-value ``None`` follows field requiredness;
        ``None`` items inside a multiple value are never accepted, while empty
        optional items converted to ``None`` are omitted from the result.
        """

        if self.is_multiple:
            if value is None:
                if self.is_required:
                    raise ValueError(f"Field {self.attr_name!r} is required.")

                return None

            if not self.is_iterable(value):
                raise TypeError(f"Field {self.attr_name!r} expects an iterable value.")

            files: List[_BFileT] = []

            for item in value:
                if item is None:
                    raise ValueError(f"Field {self.attr_name!r} does not allow None items.")

                file = self._convert_from_bitrix(item, instance=instance)

                if file is not None:
                    files.append(file)

            return files

        return self._convert_from_bitrix(value, instance=instance)

    def _convert_from_bitrix(
            self,
            value: Optional[Any],
            *,
            instance: "BaseObject" = MISSING,
    ) -> Optional[_BFileT]:
        """Create one validated file-schema object with portal context.

        Empty scalar values use the field's existing optional/required semantics.
        A non-empty remote value requires an owning SDK object because its client
        supplies the portal domain. The schema factory's return type is checked
        to catch broken custom implementations at the descriptor boundary.
        """

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if instance is MISSING:
            raise ValueError(
                f"Field {self.attr_name!r} requires an owning object to create a remote file.",
            )

        file = self._file_class.from_bitrix(
            value,
            domain=instance.client.get_token().domain,
        )

        if not isinstance(file, self._file_class):
            raise TypeError(
                f"{self._file_class.__name__}.from_bitrix() must return "
                f"{self._file_class.__name__}, got {type(file).__name__}.",
            )

        return file

    def _convert_to_bitrix(self, value: Optional[_BFileT]) -> Optional[Any]:
        """Convert one file object to its Bitrix24 write representation."""

        if not value:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, self._file_class):
            raise TypeError(
                f"Field {self.attr_name!r} expects an instance of "
                f"{self._file_class.__name__}, got {type(value).__name__}.",
            )

        return value.to_bitrix()
