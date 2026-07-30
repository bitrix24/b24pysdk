from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Generator, Generic, List, NoReturn, Type, Union

from ...schemas.api import ListFastResponseData, ListResponseData, ResponseData
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAResultT, BAValueResponseT, BValueT
from ...utils.types import JSONGenerator, JSONList
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
class AbstractBitrixAPIValueResponse(AbstractBitrixResponse[BAResultT], ABC, Generic[BAResultT, BValueT]):
    """
    Base marker for Bitrix24 API responses that expose an adapted view.

    Concrete subclasses keep the raw ``result`` contract from
    ``AbstractBitrixResponse`` and expose Python-friendly data through
    ``value`` or ``values``.
    """

    if TYPE_CHECKING:
        _result_adapter: Callable[[BAResultT], Union[BValueT, List[BValueT], Generator[BValueT, None, None]]]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIBaseValueResponse(BitrixAPIResponse[BAResultT], AbstractBitrixAPIValueResponse[BAResultT, BValueT], ABC, Generic[BAResultT, BValueT]):
    """
    Base Bitrix24 API response with a Python-friendly view over ``result``.

    ``result`` keeps the raw Bitrix24 payload. Subclasses expose adapted data
    through ``value`` or ``values`` using the stored ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], Union[BValueT, List[BValueT]]]

    @classmethod
    def from_dict(
            cls: Type[BAValueResponseT],
            json_response: ResponseData,
            /,
            *,
            result_adapter: Callable[[BAResultT], Union[BValueT, List[BValueT]]] = _missing_result_adapter,
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

@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValueResponse(BitrixAPIBaseValueResponse[BAResultT, BValueT], Generic[BAResultT, BValueT]):
    """
    Bitrix24 API response with a single adapted value.

    ``result`` keeps the raw Bitrix24 payload. ``value`` returns the
    Python-friendly object produced by ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], BValueT]

    @property
    def value(self) -> BValueT:
        """
        Return adapted Python-friendly value.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValuesResponse(BitrixAPIBaseValueResponse[BAResultT, BValueT], Generic[BAResultT, BValueT]):
    """
    Bitrix24 API response with adapted values collection.

    ``result`` keeps the raw Bitrix24 payload. ``values`` returns a list of
    Python-friendly objects produced by ``result_adapter``.
    """

    _result_adapter: Callable[[BAResultT], List[BValueT]]

    @property
    def values(self) -> List[BValueT]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIValuesListResponse(BitrixAPIListResponse, AbstractBitrixAPIValueResponse[JSONList, BValueT], Generic[BValueT]):
    """
    Bitrix24 list response with adapted values collection.

    Unlike ``BitrixAPIValuesResponse``, this response intentionally follows the
    regular ``BitrixAPIListResponse`` shape: it stores only ``result`` and
    ``time`` and does not expose Bitrix pagination fields such as ``next`` and
    ``total``. ``result`` keeps the raw fully loaded list returned by
    ``call_list``.
    """

    _result_adapter: Callable[[JSONList], List[BValueT]]

    @property
    def values(self) -> List[BValueT]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)

    @classmethod
    def from_dict(
            cls,
            json_response: ListResponseData,
            /,
            *,
            result_adapter: Callable[[JSONList], List[BValueT]] = _missing_result_adapter,
    ) -> "BitrixAPIValuesListResponse[BValueT]":
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

    def to_dict(self) -> ListResponseData:
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
class BitrixAPIValuesListFastResponse(BitrixAPIListFastResponse, AbstractBitrixAPIValueResponse[JSONGenerator, BValueT], Generic[BValueT]):
    """
    Fast Bitrix24 list response with adapted values collection.

    ``result`` keeps the lazy one-time generator returned by
    ``call_list_fast``. ``values`` is adapted from that generator using
    ``result_adapter``. Timing metadata is kept mutable, matching
    ``BitrixAPIListFastResponse`` behavior.
    """

    _result_adapter: Callable[[JSONGenerator], Generator[BValueT, None, None]] = _missing_result_adapter

    @property
    def values(self) -> Generator[BValueT, None, None]:
        """
        Return adapted Python-friendly values.

        The conversion is performed on each property access.
        """
        return self._result_adapter(self.result)

    @classmethod
    def from_dict(
            cls,
            json_response: ListFastResponseData,
            /,
            *,
            result_adapter: Callable[[JSONGenerator], Generator[BValueT, None, None]] = _missing_result_adapter,
    ) -> "BitrixAPIValuesListFastResponse[BValueT]":
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
