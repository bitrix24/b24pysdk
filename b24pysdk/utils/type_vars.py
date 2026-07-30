import enum
import typing

if typing.TYPE_CHECKING:
    from ..api import requests as _requests
    from ..api import responses as _responses
    from ..objects._base_object import BaseObject
    from ..schemas._base_schema import BaseSchema
    from ..schemas._base_schema_dict import BaseSchemaDict
    from . import types as _types

__all__ = [
    "BOPKT",
    "BOT",
    "BST",
    "BABatchRequestsT",
    "BAListResponseT",
    "BAListResultT",
    "BARequestT",
    "BAResponseT",
    "BAResultT",
    "BAValueResponseT",
    "BEnumT",
    "BRawT",
    "BResponseT",
    "BSDataT",
    "BSDictT",
    "BValueT",
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

BRawT = typing.TypeVar("BRawT")
"""Type variable for a raw Bitrix24 field value."""

BSDataT = typing.TypeVar("BSDataT")
"""Type variable for raw data used to build SDK schema objects."""

BSDictT = typing.TypeVar("BSDictT", bound="BaseSchemaDict")
"""Type variable for dictionary-like SDK schema classes."""

BST = typing.TypeVar("BST", bound="BaseSchema")
"""Type variable for SDK schema classes."""

BValueT = typing.TypeVar("BValueT")
"""Type variable for a Python value exposed by an SDK field or produced by a result adapter."""

BOT = typing.TypeVar("BOT", bound="BaseObject")
"""Type variable for SDK object classes."""

BOPKT = typing.TypeVar("BOPKT", bound="typing.Hashable")
"""Type variable for an SDK object primary-key value."""

BResponseT = typing.TypeVar("BResponseT")
"""Type variable that preserves concrete return types across generic helper methods."""

BEnumT = typing.TypeVar("BEnumT", bound=enum.Enum)
"""Type variable for stdlib enum classes used by SDK fields."""
