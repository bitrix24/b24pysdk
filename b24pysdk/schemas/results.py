from typing import TypedDict

__all__ = [
    "CountResultData",
    "IDResultData",
]


class CountResultData(TypedDict):
    count: int


class IDResultData(TypedDict):
    id: int
