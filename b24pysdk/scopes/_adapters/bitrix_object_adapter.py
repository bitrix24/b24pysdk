from typing import TYPE_CHECKING, Generator, Generic, List, NoReturn, Optional, Text, Tuple, Type, Union, overload

from ...objects import BitrixObjectList
from ...utils.type_vars import BOT
from ...utils.types import JSONDict, JSONList

_BitrixObjectResult = Optional[Union[JSONDict, Text, int]]
_BitrixUnwrappedResult = Optional[Union[JSONDict, JSONList, Text, int]]

if TYPE_CHECKING:
    from ...client import ClientType

__all__ = [
    "BitrixObjectAdapter",
    "BitrixObjectsAdapter",
]


class BitrixObjectAdapter(Generic[BOT]):
    """Adapter converting one Bitrix24 object result to an SDK object."""

    __slots__ = ("_client", "_object_class", "_wrapper")

    _client: "ClientType"
    _object_class: Type[BOT]
    _wrapper: Optional[Text]

    def __init__(
            self,
            object_class: Type[BOT],
            *,
            client: "ClientType",
            wrapper: Optional[Text] = None,
    ):
        self._object_class = object_class
        self._client = client
        self._wrapper = wrapper

    @overload
    def __call__(self, bitrix_result: None) -> None: ...

    @overload
    def __call__(self, bitrix_result: Union[JSONDict, Text, int]) -> BOT: ...

    def __call__(self, bitrix_result: _BitrixObjectResult, /) -> Optional[BOT]:
        """Convert one Bitrix24 object payload, wrapped payload, or object id."""

        if self._wrapper is not None:
            return self._adapt_result(self._unwrap_result(bitrix_result))

        return self._adapt_result(bitrix_result)

    def _adapt_result(self, bitrix_result: _BitrixUnwrappedResult, /) -> Optional[BOT]:
        """Convert an already explicitly unwrapped Bitrix24 result."""

        if bitrix_result is None:
            return None

        if isinstance(bitrix_result, dict):
            return self._make_object_from_dict(bitrix_result)

        if isinstance(bitrix_result, (str, int)) and not isinstance(bitrix_result, bool):
            return self._make_object_from_pk(bitrix_result)

        raise TypeError(
            "Expected Bitrix24 object result to be a dict, str, int, or None, "
            f"got {type(bitrix_result).__name__}.",
        )

    def _make_object_from_dict(self, bitrix_result: JSONDict, /) -> BOT:
        """Convert object data, primary-key data, or a single-key wrapper."""

        pk_bitrix_codes = self._get_pk_bitrix_codes()

        if set(pk_bitrix_codes).issubset(bitrix_result):
            bitrix_pk_values = tuple(bitrix_result[bitrix_code] for bitrix_code in pk_bitrix_codes)

            if any(value is None for value in bitrix_pk_values):
                raise TypeError(
                    f"Expected {self._object_class.__name__} primary-key fields not to contain None.",
                )

            bitrix_pk = self._object_class._meta.build_bitrix_pk(*bitrix_pk_values)
            bitrix_data = None if set(bitrix_result) == set(pk_bitrix_codes) else dict(bitrix_result)

            return self._object_class(
                bitrix_pk=bitrix_pk,
                bitrix_data=bitrix_data,
                client=self._client,
            )

        if len(bitrix_result) == 1:
            wrapped_result = next(iter(bitrix_result.values()))
            bitrix_object = self._adapt_result(wrapped_result)

            if bitrix_object is None:
                raise TypeError("Expected wrapped Bitrix24 object result not to be None.")

            return bitrix_object

        raise TypeError(
            f"Expected {self._object_class.__name__} result to contain all primary-key fields "
            "or exactly one wrapper key.",
        )

    def _make_object_from_pk(self, bitrix_pk: Union[Text, int], /) -> BOT:
        """Convert a scalar result to an object with a simple primary key."""

        pk_bitrix_codes = self._get_pk_bitrix_codes()

        if len(pk_bitrix_codes) != 1:
            raise TypeError(
                f"Scalar primary key cannot be used for {self._object_class.__name__} "
                "with a composite primary key.",
            )

        return self._object_class(bitrix_pk=bitrix_pk, client=self._client)

    def _make_object(self, bitrix_data: JSONDict) -> BOT:
        """Convert one full Bitrix24 item to an SDK object."""
        return self._make_object_from_dict(bitrix_data)

    def _get_pk_bitrix_codes(self) -> Tuple[Text, ...]:
        """Return primary-key Bitrix24 codes in their registered order."""

        pk_bitrix_codes = tuple(
            bitrix_field.bitrix_code
            for bitrix_field in self._object_class._meta.pk_fields
        )

        if not pk_bitrix_codes:
            raise TypeError(f"{self._object_class.__name__} has no primary-key fields.")

        return pk_bitrix_codes

    def _unwrap_result(self, bitrix_result: _BitrixObjectResult, /) -> _BitrixUnwrappedResult:
        """Extract value stored under the explicitly configured wrapper key."""

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                "Expected wrapped Bitrix24 result to be a dict, "
                f"got {type(bitrix_result).__name__}.",
            )

        if self._wrapper not in bitrix_result:
            raise TypeError(f"Expected wrapper {self._wrapper!r} in Bitrix24 result.")

        return bitrix_result[self._wrapper]


class BitrixObjectsAdapter(BitrixObjectAdapter[BOT], Generic[BOT]):
    """Adapter converting Bitrix24 list-like results to SDK objects."""

    @overload
    def __call__(self, bitrix_result: None) -> BitrixObjectList[NoReturn]: ...

    @overload
    def __call__(self, bitrix_result: List[JSONDict]) -> BitrixObjectList[BOT]: ...

    @overload
    def __call__(self, bitrix_result: Generator[JSONDict, None, None]) -> Generator[BOT, None, None]: ...

    @overload
    def __call__(self, bitrix_result: JSONDict) -> BitrixObjectList[BOT]: ...

    def __call__(
            self,
            bitrix_result: Optional[Union[List[JSONDict], Generator[JSONDict, None, None], JSONDict]],
            /,
    ) -> Union[BitrixObjectList[BOT], Generator[BOT, None, None]]:
        """Convert a list-like Bitrix24 result to SDK objects."""

        if bitrix_result is None:
            return BitrixObjectList().using(client=self._client)

        if isinstance(bitrix_result, list):
            return BitrixObjectList(self._make_object(bitrix_data) for bitrix_data in bitrix_result).using(client=self._client)

        if isinstance(bitrix_result, dict):
            return BitrixObjectList(self._make_object(bitrix_data) for bitrix_data in self._unwrap_list_result(bitrix_result)).using(client=self._client)

        return (self._make_object(bitrix_data) for bitrix_data in bitrix_result)

    def _unwrap_list_result(self, bitrix_result: JSONDict, /) -> List[JSONDict]:
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
