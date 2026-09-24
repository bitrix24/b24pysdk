from typing import (
    TYPE_CHECKING,
    FrozenSet,
    Generator,
    Generic,
    Iterable,
    List,
    NoReturn,
    Optional,
    Text,
    Type,
    Union,
    overload,
)

from ..._config import Config
from ...objects import BitrixObjectList, ClientProvider
from ...utils.type_vars import BOT
from ...utils.types import JSONDict, JSONList, ObjectDiscriminator

if TYPE_CHECKING:
    from ...client import ClientType
    from ...objects._object_metadata import ObjectMetadata

__all__ = [
    "BitrixObjectAdapter",
    "BitrixObjectsAdapter",
]


class BitrixObjectAdapter(Generic[BOT]):
    """Adapter converting one Bitrix24 object result to an SDK object."""

    __slots__ = (
        "_client_provider",
        "_discriminator",
        "_object_key",
        "_select",
        "_wrapper",
    )

    _client_provider: ClientProvider
    _discriminator: ObjectDiscriminator
    _object_key: Text
    _select: Optional[FrozenSet[Text]]
    _wrapper: Optional[Text]

    def __init__(
            self,
            object_key: Text,
            *,
            client: "ClientType",
            select: Optional[Iterable[Text]] = None,
            discriminator: ObjectDiscriminator = None,
            wrapper: Optional[Text] = None,
    ):
        """Initialize an adapter with the effective Bitrix24 field selection.

        When ``select`` is ``None``, completeness is determined by the object
        metadata flag copied from ``_IS_COMPLETE_WITHOUT_SELECT``. Otherwise,
        the iterable must contain the effective Bitrix24 field codes returned
        by the API. The selection is materialized once for all adapted values.
        """
        self._object_key = object_key
        self._client_provider = ClientProvider(client=client)
        self._discriminator = discriminator
        self._wrapper = wrapper
        self._select = None if select is None else frozenset(select)

    @overload
    def __call__(self, bitrix_result: None) -> None: ...

    @overload
    def __call__(self, bitrix_result: Union[JSONDict, Text, int]) -> BOT: ...

    def __call__(self, bitrix_result: Optional[Union[JSONDict, Text, int]], /) -> Optional[BOT]:
        """Convert one Bitrix24 object payload, wrapped payload, or object id."""

        if bitrix_result is None:
            return None

        if self._wrapper is not None:
            return self._adapt_result(self._unwrap_result(bitrix_result))

        return self._adapt_result(bitrix_result)

    def _adapt_result(self, bitrix_result: Optional[Union[JSONDict, Text, int]], /) -> BOT:
        """Convert an already unwrapped Bitrix24 result."""

        if isinstance(bitrix_result, (dict, str, int)) and not isinstance(bitrix_result, bool):
            return self._make_object(bitrix_result)

        raise TypeError(
            "Expected Bitrix24 object data or primary key to be "
            f"a dict, str, or int, got {type(bitrix_result).__name__}.",
        )

    def _make_object(self, bitrix_data_or_pk: Union[JSONDict, Text, int]) -> BOT:
        """Convert Bitrix24 object data or primary key to an SDK object."""

        object_meta = self._get_object_class().get_meta()

        return object_meta.make_object_from_bitrix_data_or_pk(
            bitrix_data_or_pk,
            client_provider=self._client_provider,
            bitrix_data_is_complete=self._is_bitrix_data_complete(object_meta),
        )

    def _is_bitrix_data_complete(self, object_meta: "ObjectMetadata[BOT]") -> bool:
        """Return whether the effective selection covers every object field."""

        if self._select is None:
            return object_meta.is_complete_without_select

        return object_meta.contains_all_fields(self._select)

    def _unwrap_result(self, bitrix_result: JSONDict, /) -> Union[JSONDict, JSONList, Text, int]:
        """Extract value stored under the explicitly configured wrapper key."""

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                "Expected wrapped Bitrix24 result to be a dict, "
                f"got {type(bitrix_result).__name__}.",
            )

        if self._wrapper not in bitrix_result:
            raise TypeError(f"Expected wrapper {self._wrapper!r} in Bitrix24 result.")

        return bitrix_result[self._wrapper]

    def _get_object_class(self) -> Type[BOT]:
        """Return the currently registered SDK object class."""
        return Config.get_object_class(object_key=self._object_key, discriminator=self._discriminator)


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
            return BitrixObjectList(client_provider=self._client_provider)

        object_meta = self._get_object_class().get_meta()
        make_object = object_meta.make_object_from_bitrix_data_or_pk
        client_provider = self._client_provider
        bitrix_data_is_complete = self._is_bitrix_data_complete(object_meta)

        if isinstance(bitrix_result, list):
            return BitrixObjectList(
                (
                    make_object(
                        bitrix_data,
                        client_provider=client_provider,
                        bitrix_data_is_complete=bitrix_data_is_complete,
                    )
                    for bitrix_data in bitrix_result
                ),
                client_provider=client_provider,
            )

        if isinstance(bitrix_result, dict):
            return BitrixObjectList(
                (
                    make_object(
                        bitrix_data,
                        client_provider=client_provider,
                        bitrix_data_is_complete=bitrix_data_is_complete,
                    )
                    for bitrix_data in self._unwrap_list_result(bitrix_result)
                ),
                client_provider=client_provider,
            )

        return (
            make_object(
                bitrix_data,
                client_provider=client_provider,
                bitrix_data_is_complete=bitrix_data_is_complete,
            )
            for bitrix_data in bitrix_result
        )

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
