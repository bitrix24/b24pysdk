from dataclasses import asdict, dataclass
from typing import Dict, List, Text, Union

from ..._constants import PYTHON_VERSION
from ...utils.types import B24APIResult, JSONDict, JSONList
from .abstract_bitrix_response import AbstractBitrixResponse
from .bitrix_time_response import BitrixTimeResponse

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True

__all__ = [
    "B24APIBatchResult",
    "BitrixAPIBatchResponse",
]


@dataclass(**_DATACLASS_KWARGS)
class B24APIBatchResult:
    """
    Result payload of a Bitrix24 batch response.

    Stores per-command batch results, errors, pagination metadata, and timing
    data. The collection shape follows the original batch request shape:
    mapping requests produce mapping results, while sequence requests produce
    list results.
    """

    result: Union[Dict[Text, B24APIResult], List[B24APIResult]]
    result_error: Union[JSONDict, JSONList]
    result_total: Union[Dict[Text, int], List[int]]
    result_next: Union[Dict[Text, int], List[int]]
    result_time: Union[Dict[Text, BitrixTimeResponse], List[BitrixTimeResponse]]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result=<{type(self.result).__name__}: {len(self.result)}>, "
            f"result_error=<{type(self.result_error).__name__}: {len(self.result_error)}>, "
            f"result_total=<{type(self.result_total).__name__}: {len(self.result_total)}>, "
            f"result_next=<{type(self.result_next).__name__}: {len(self.result_next)}>, "
            f"result_time=<{type(self.result_time).__name__}: {len(self.result_time)}>)"
        )

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "B24APIBatchResult":
        """
        Create a B24APIBatchResult instance from raw batch result data.

        Args:
            json_response: Raw ``result`` section of a Bitrix24 batch response.

        Returns:
            Parsed batch result payload.
        """

        json_result_time = json_response["result_time"]

        if isinstance(json_result_time, dict):
            result_time = {}

            for key, time_value in json_result_time.items():
                result_time[key] = BitrixTimeResponse.from_dict(time_value)

        else:
            result_time = []

            for time_value in json_result_time:
                result_time.append(BitrixTimeResponse.from_dict(time_value))

        return cls(
            result=json_response["result"],
            result_error=json_response["result_error"],
            result_total=json_response["result_total"],
            result_next=json_response["result_next"],
            result_time=result_time,
        )

    def to_dict(self) -> JSONDict:
        """
        Convert batch result payload to dictionary.

        Returns:
            Dictionary representation of the batch result.
        """
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIBatchResponse(AbstractBitrixResponse[B24APIBatchResult]):
    """
    Typed Bitrix24 batch response.

    Contains parsed batch command results in ``result`` and aggregated Bitrix24
    timing metadata in ``time``.
    """

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAPIBatchResponse":
        """
        Create a BitrixAPIBatchResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by Bitrix24 batch call.

        Returns:
            Parsed Bitrix batch response.
        """
        return cls(
            result=B24APIBatchResult.from_dict(json_response["result"]),
            time=cls._convert_time(json_response["time"]),
        )
