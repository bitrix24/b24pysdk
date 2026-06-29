from typing import TypedDict

from ..results import IDResultData

__all__ = [
    "ConfigurableActivityResultData",
]


class ConfigurableActivityResultData(TypedDict):
    activity: IDResultData
