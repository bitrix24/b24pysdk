from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Generator, Generic, List, NoReturn, Type, Union

from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAResultT, BAValueResponseT, BAValueT
from ...utils.types import JSONDict, JSONGenerator, JSONList
from .abstract_bitrix_response import AbstractBitrixResponse
from .bitrix_api_list_response import BitrixAPIListFastResponse, BitrixAPIListResponse
from .bitrix_api_response import BitrixAPIResponse

__all__ = [
    "AbstractBitrixAPIValueResponse",
    "BitrixAPIBaseValueResponse",
    "BitrixAPIValueResponse",
    "BitrixAPIValuesListFastResponse",
    "BitrixAPIValuesListResponse",
    "BitrixAPIValuesResponse",
]


def _missing_result_adapter(_: BAResultT, /) -> NoReturn:
    raise RuntimeError("Result adapter is required for value response.")


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class AbstractBitrixAPIValueResponse(AbstractBitrixResponse[BAResultT], ABC, Generic[BAResultT, BAValueT]):
    """
    Base marker for Bitrix24 API responses that expose an adapted view.

    Concrete subclasses keep the raw ``result`` contract from
    ``AbstractBitrixResponse`` and expose Python-friendly data through
    ``value`` or ``values``.
    """

    if TYPE_CHECKING:
        _result_adapter: Callable[[BAResultT], Union[BAValueT, List[BAValueT], Generator[BAValueT, None, None]]]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIBaseValueResponse(BitrixAPIResponse[BAResultT], AbstractBitrixAPIValueResponse[BAResultT, BAValueT], ABC, Generic[BAResultT, BAValueT]):
    """
    Base Bitrix24 API response with a Python-friendly view over ``result``.

    ``result`` keeps the raw Bitrix24 payload. Subclasses expose adapted data
    through ``value`` or ``values`` using the stored ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], Union[BAValueT, List[BAValueT]]]

    @classmethod
    def from_dict(
            cls: Type[BAValueResponseT],
            json_response: JSONDict,
            /,
            *,
            result_adapter: Callable[[BAResultT], Union[BAValueT, List[BAValueT]]] = _missing_result_adapter,
    ) -> BAValueResponseT:
        """
        Create an adapted response from raw JSON response.

        Args:
            json_response: Raw JSON response returned by Bitrix24.
            result_adapter: Callable converting raw ``result`` to adapted data.

        Returns:
            Parsed API response with adapted data access.
        """
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
            next=json_response.get("next"),
            total=json_response.get("total"),
            _result_adapter=result_adapter,
        )

    def to_dict(self) -> JSONDict:
        """
        Convert response to a JSON-compatible dictionary.

        Internal adapter field is intentionally excluded from the serialized
        representation.
        """
        return {
            "result": self.result,
            "time": self.time.to_dict(),
            "next": self.next,
            "total": self.total,
        }


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValueResponse(BitrixAPIBaseValueResponse[BAResultT, BAValueT], Generic[BAResultT, BAValueT]):
    """
    Bitrix24 API response with a single adapted value.

    ``result`` keeps the raw Bitrix24 payload. ``value`` returns the
    Python-friendly object produced by ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], BAValueT]

    @property
    def value(self) -> BAValueT:
        """
        Return adapted Python-friendly value.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValuesResponse(BitrixAPIBaseValueResponse[BAResultT, List[BAValueT]], Generic[BAResultT, BAValueT]):
    """
    Bitrix24 API response with adapted values collection.

    ``result`` keeps the raw Bitrix24 payload. ``values`` returns a list of
    Python-friendly objects produced by ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], List[BAValueT]]

    @property
    def values(self) -> List[BAValueT]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValuesListResponse(BitrixAPIListResponse, AbstractBitrixAPIValueResponse[JSONList, List[BAValueT]], Generic[BAValueT]):
    """
    Bitrix24 list response with adapted values collection.

    Unlike ``BitrixAPIValuesResponse``, this response intentionally follows the
    regular ``BitrixAPIListResponse`` shape: it stores only ``result`` and
    ``time`` and does not expose Bitrix pagination fields such as ``next`` and
    ``total``. ``result`` keeps the raw fully loaded list returned by
    ``call_list``.
    """

    _result_adapter: Callable[[JSONList], List[BAValueT]]

    @property
    def values(self) -> List[BAValueT]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)

    @classmethod
    def from_dict(
            cls,
            json_response: JSONDict,
            /,
            *,
            result_adapter: Callable[[JSONList], List[BAValueT]] = _missing_result_adapter,
    ) -> "BitrixAPIValuesListResponse[BAValueT]":
        """
        Create an adapted list response from raw JSON response.

        Args:
            json_response: Raw JSON response returned by ``call_list``.
            result_adapter: Callable converting raw list ``result`` to adapted
                values.

        Returns:
            Parsed list response with adapted ``values`` access.
        """
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
            _result_adapter=result_adapter,
        )

    def to_dict(self) -> JSONDict:
        """
        Convert list response to a JSON-compatible dictionary.

        Internal adapter field is intentionally excluded from the serialized
        representation.
        """
        return {
            "result": self.result,
            "time": self.time.to_dict(),
        }


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValuesListFastResponse(BitrixAPIListFastResponse, AbstractBitrixAPIValueResponse[JSONGenerator, Generator[BAValueT, None, None]], Generic[BAValueT]):
    """
    Fast Bitrix24 list response with adapted values collection.

    ``result`` keeps the lazy one-time generator returned by
    ``call_list_fast``. ``values`` is adapted from that generator using
    ``result_adapter``. Timing metadata is kept mutable, matching
    ``BitrixAPIListFastResponse`` behavior.
    """

    _result_adapter: Callable[[JSONGenerator], Generator[BAValueT, None, None]] = _missing_result_adapter

    @property
    def values(self) -> Generator[BAValueT, None, None]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)

    @classmethod
    def from_dict(
            cls,
            json_response: JSONDict,
            /,
            *,
            result_adapter: Callable[[JSONGenerator], Generator[BAValueT, None, None]] = _missing_result_adapter,
    ) -> "BitrixAPIValuesListFastResponse[BAValueT]":
        """
        Create an adapted fast list response from raw JSON response.

        Args:
            json_response: Raw JSON response returned by ``call_list_fast``.
            result_adapter: Callable converting raw generator ``result`` to
                adapted values.

        Returns:
            Parsed fast list response with adapted ``values`` access.
        """
        return cls(
            result=json_response["result"],
            time=json_response["time"],
            _result_adapter=result_adapter,
        )
