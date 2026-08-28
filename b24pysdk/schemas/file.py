from typing import Optional, Text, TypedDict

__all__ = [
    "BitrixFileResponseData",
]


class BitrixFileResponseData(TypedDict):
    """Data returned by a successful Bitrix24 file download."""
    content: bytes
    name: Optional[Text]
