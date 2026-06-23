import typing

if typing.TYPE_CHECKING:
    from ..api import requests as _requests
    from ..api import responses as _responses

    # noinspection PyProtectedMember
    from ..schemas._base_listable_schema import BaseListableSchema

    # noinspection PyProtectedMember
    from ..schemas._base_schema import BaseSchema
    from . import types as _types

__all__ = [
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
"""Bitrix API batch requests collection type."""

BAListResponseT = typing.TypeVar("BAListResponseT", bound="_responses.AbstractBitrixAPIListResponse")
"""Bitrix API list response type."""

BAListResultT = typing.TypeVar("BAListResultT", bound=typing.Iterable["_types.JSONDict"])
"""Bitrix API list result type, represented as an iterable of JSON objects."""

BARequestT = typing.TypeVar("BARequestT", bound="_requests.AbstractBitrixAPIRequest")
"""Bitrix API request type."""

BAResponseT = typing.TypeVar("BAResponseT", bound="_responses.AbstractBitrixResponse")
"""Bitrix API response type."""

BAResultT = typing.TypeVar("BAResultT")
"""Bitrix API raw result type."""

BAValueResponseT = typing.TypeVar("BAValueResponseT", bound="_responses.AbstractBitrixAPIValueResponse")
"""Bitrix API value response type."""

BAValueT = typing.TypeVar("BAValueT")
"""Bitrix API adapted value type."""

BSDataT = typing.TypeVar("BSDataT")
"""Bitrix schema data type."""

BSLT = typing.TypeVar("BSLT", bound="BaseListableSchema")
"""Bitrix listable schema type."""

BST = typing.TypeVar("BST", bound="BaseSchema")
"""Bitrix schema type."""

ResponseT = typing.TypeVar("ResponseT")
"""Generic response type used by abstract request classes."""
