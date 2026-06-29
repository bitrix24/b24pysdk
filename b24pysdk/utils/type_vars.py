import typing

if typing.TYPE_CHECKING:
    from ..api import requests as _requests
    from ..api import responses as _responses
    from ..schemas._base_listable_schema import BaseListableSchema
    from ..schemas._base_schema import BaseSchema
    from ..schemas._base_schema_dict import BaseSchemaDict
    from . import types as _types

__all__ = [
    "BSDT",
    "BSLT",
    "BST",
    "BABatchRequestsT",
    "BAListResponseT",
    "BAListResultT",
    "BARequestT",
    "BAResponseT",
    "BAResultT",
    "BAValueResponseT",
    "BAValueT",
    "BSDataT",
    "ResponseT",
]

BABatchRequestsT = typing.TypeVar(
    "BABatchRequestsT",
    bound=typing.Union[
        typing.Mapping["_types.Key", "_requests.BitrixAPIRequest"],
        typing.Sequence["_requests.BitrixAPIRequest"],
    ],
)
"""Type variable for a Bitrix API batch request collection."""

BAListResponseT = typing.TypeVar("BAListResponseT", bound="_responses.AbstractBitrixAPIListResponse")
"""Type variable for SDK responses that load list-like API results."""

BAListResultT = typing.TypeVar("BAListResultT", bound=typing.Iterable["_types.JSONDict"])
"""Type variable for raw list results represented as iterable JSON objects."""

BARequestT = typing.TypeVar("BARequestT", bound="_requests.AbstractBitrixAPIRequest")
"""Type variable for SDK request wrapper classes."""

BAResponseT = typing.TypeVar("BAResponseT", bound="_responses.AbstractBitrixResponse")
"""Type variable for SDK response wrapper classes."""

BAResultT = typing.TypeVar("BAResultT")
"""Type variable for an unadapted ``result`` payload returned by Bitrix24."""

BAValueResponseT = typing.TypeVar("BAValueResponseT", bound="_responses.AbstractBitrixAPIValueResponse")
"""Type variable for SDK responses that expose an adapted ``value`` or ``values`` property."""

BAValueT = typing.TypeVar("BAValueT")
"""Type variable for a value produced by a result adapter."""

BSDataT = typing.TypeVar("BSDataT")
"""Type variable for raw data used to build SDK schema objects."""

BSDT = typing.TypeVar("BSDT", bound="BaseSchemaDict")
"""Type variable for dictionary-like SDK schema classes."""

BST = typing.TypeVar("BST", bound="BaseSchema")
"""Type variable for SDK schema classes."""

BSLT = typing.TypeVar("BSLT", bound="BaseListableSchema")
"""Type variable for SDK schema classes that can be used in list results."""

ResponseT = typing.TypeVar("ResponseT")
"""Type variable that preserves concrete return types across generic helper methods."""
