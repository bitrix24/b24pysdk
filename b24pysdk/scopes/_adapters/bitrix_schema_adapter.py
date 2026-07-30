from typing import Dict, Generator, Generic, List, NoReturn, Optional, Text, Type, Union, overload

from ...utils.type_vars import BST, BSDataT
from ...utils.types import JSONDict

__all__ = [
    "BitrixSchemaAdapter",
    "BitrixSchemasAdapter",
]


class BitrixSchemaAdapter(Generic[BSDataT, BST]):
    """Adapter converting one Bitrix24 object result to an SDK schema."""

    __slots__ = ("_schema_class", "_wrapper")

    _schema_class: Type[BST]
    _wrapper: Optional[Text]

    def __init__(self, schema_class: Type[BST], *, wrapper: Optional[Text] = None):
        self._schema_class = schema_class
        self._wrapper = wrapper

    def __call__(self, bitrix_result: Union[BSDataT, Dict[Text, BSDataT]], /) -> BST:
        """Convert one Bitrix24 result to a schema instance."""

        if self._wrapper is not None:
            bitrix_result = self._unwrap_result(bitrix_result)

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                f"Expected Bitrix24 result to be a dict, got {type(bitrix_result).__name__}.",
            )

        return self._make_schema(bitrix_result)

    def _make_schema(self, bitrix_data: BSDataT) -> BST:
        """Convert one Bitrix24 item to an SDK schema."""
        return self._schema_class.from_bitrix(bitrix_data)

    def _unwrap_result(self, bitrix_result: Dict[Text, BSDataT], /) -> Union[BSDataT, List[BSDataT]]:
        """Extract value stored under the configured wrapper key."""

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                "Expected wrapped Bitrix24 result to be a dict, "
                f"got {type(bitrix_result).__name__}.",
            )

        if self._wrapper not in bitrix_result:
            raise TypeError(f"Expected wrapper {self._wrapper!r} in Bitrix24 result.")

        return bitrix_result[self._wrapper]


class BitrixSchemasAdapter(BitrixSchemaAdapter[BSDataT, BST], Generic[BSDataT, BST]):
    """Adapter converting Bitrix24 list-like results to SDK schemas."""

    @overload
    def __call__(self, bitrix_result: None) -> List[NoReturn]: ...

    @overload
    def __call__(self, bitrix_result: List[BSDataT]) -> List[BST]: ...

    @overload
    def __call__(self, bitrix_result: Generator[BSDataT, None, None]) -> Generator[BST, None, None]: ...

    @overload
    def __call__(self, bitrix_result: JSONDict) -> List[BST]: ...

    def __call__(
            self,
            bitrix_result: Optional[Union[List[BSDataT], Generator[BSDataT, None, None], JSONDict]],
    ) -> Union[List[BST], Generator[BST, None, None]]:
        """Convert a list-like Bitrix24 result to schema instances."""

        if bitrix_result is None:
            return []

        if isinstance(bitrix_result, list):
            return [self._make_schema(bitrix_data) for bitrix_data in bitrix_result]

        if isinstance(bitrix_result, dict):
            return [self._make_schema(bitrix_data) for bitrix_data in self._unwrap_list_result(bitrix_result)]

        return (self._make_schema(bitrix_data) for bitrix_data in bitrix_result)

    def _unwrap_list_result(self, bitrix_result: JSONDict, /) -> List[BSDataT]:
        """Extract a list from a wrapped Bitrix24 result."""

        if self._wrapper is None:
            raise TypeError(
                "Expected explicit wrapper for wrapped Bitrix24 list result. "
                f"Got {type(bitrix_result).__name__}.",
            )

        unwrapped_result = self._unwrap_result(bitrix_result)

        if not isinstance(unwrapped_result, list):
            raise TypeError(
                f"Expected wrapped Bitrix24 result under {self._wrapper!r} "
                f"to be a list, got {type(unwrapped_result).__name__}.",
            )

        return unwrapped_result
