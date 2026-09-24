from typing import TYPE_CHECKING, Generic, List, Optional, Text, Type, Union

from ...schemas._base_schema import BaseSchema
from ...utils.type_vars import BST
from ...utils.types import JSONDict
from .._filter_lookups import NO_FILTER_OPERATORS
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "BitrixSchemaField",
]


class BitrixSchemaField(BaseField[JSONDict, BST], Generic[BST]):
    """
    Field that exposes a Bitrix24 dictionary as a ``BaseSchema`` instance.

    ``schema_class`` must be a ``BaseSchema`` subclass whose ``from_bitrix()``
    accepts a dictionary and whose ``to_bitrix()`` returns a dictionary.
    Multiple field values are converted item by item by ``BaseField``.
    """

    _FILTER_OPERATORS = NO_FILTER_OPERATORS

    __slots__ = ("_schema_class",)

    _schema_class: Type[BST]

    def __init__(
            self,
            bitrix_code: Text,
            *,
            schema_class: Type[BST],
            is_pk: bool = False,
            is_required: Optional[bool] = None,
            is_multiple: bool = False,
            is_read_only: bool = False,
            is_updatable: bool = True,
            request_name: Optional[Text] = None,
    ):
        if not (isinstance(schema_class, type) and issubclass(schema_class, BaseSchema)):
            raise TypeError("schema_class must be a BaseSchema subclass.")

        super().__init__(
            bitrix_code=bitrix_code,
            is_pk=is_pk,
            is_required=is_required,
            is_multiple=is_multiple,
            is_read_only=is_read_only,
            is_updatable=is_updatable,
            request_name=request_name,
        )
        self._schema_class = schema_class

    @property
    def schema_class(self) -> Type[BST]:
        """Return the immutable schema class used by this field."""
        return self._schema_class

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["BitrixSchemaField[BST]", Optional[BST], List[BST]]: ...

    def _convert_from_bitrix(self, value: Optional[JSONDict]) -> Optional[BST]:
        """Convert one raw Bitrix24 dictionary to a schema instance."""

        if value is None:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, dict):
            raise TypeError(
                f"Field {self.attr_name!r} expects a dict from Bitrix24, "
                f"got {type(value).__name__}.",
            )

        return self._schema_class.from_bitrix(value)

    def _convert_to_bitrix(self, value: Optional[BST]) -> Optional[JSONDict]:
        """Convert one schema instance to a raw Bitrix24 dictionary."""

        if value is None:
            if self.is_required:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return None

        if not isinstance(value, self._schema_class):
            raise TypeError(
                f"Field {self.attr_name!r} expects an instance of "
                f"{self._schema_class.__name__}, got {type(value).__name__}.",
            )

        return value.to_bitrix()
