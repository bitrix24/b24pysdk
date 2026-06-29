from dataclasses import dataclass
from typing import Generic, Optional, Type

from ...schemas.api import ResponseData
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAResponseT, BAResultT
from .abstract_bitrix_response import AbstractBitrixResponse

__all__ = [
    "BitrixAPIResponse",
]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIResponse(AbstractBitrixResponse[BAResultT], Generic[BAResultT]):
    """
    Standard Bitrix24 API response.

    Represents a regular REST API response containing ``result`` and ``time``,
    with optional pagination metadata returned by list-like methods.
    """

    next: Optional[int]
    total: Optional[int]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time}, "
            f"next={self.next}, "
            f"total={self.total})"
        )

    @classmethod
    def from_dict(cls: Type[BAResponseT], json_response: ResponseData, /) -> BAResponseT:
        """
        Create a BitrixAPIResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed standard API response.
        """
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
            next=json_response.get("next"),
            total=json_response.get("total"),
        )

    def to_dict(self) -> ResponseData:
        """
        Convert response to a JSON-compatible dictionary.

        Internal adapter field is intentionally excluded from the serialized
        representation.
        """

        response_data: ResponseData = {
            "result": self.result,
            "time": self.time.to_dict(),
        }

        if self.next is not None:
            response_data["next"] = self.next

        if self.total is not None:
            response_data["total"] = self.total

        return response_data
