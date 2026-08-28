from typing import Annotated, Dict, List, Text, TypedDict, Union

from ..utils.types import B24APIResult, B24AppStatusLiteral, JSONDict, JSONGenerator, JSONList

__all__ = [
    "B24AppInfoInstallData",
    "B24AppInfoResultData",
    "BatchResponseData",
    "BatchResultData",
    "BitrixAppInfoResponseData",
    "ListFastResponseData",
    "ListResponseData",
    "ResponseData",
    "TimeResponseData",
]


class _TimeResponseOptionalData(TypedDict, total=False):
    operating_reset_at: float
    operating: float


class TimeResponseData(_TimeResponseOptionalData):
    start: float
    finish: float
    duration: float
    processing: float
    date_start: Text
    date_finish: Text


class _ResponseOptionalData(TypedDict, total=False):
    next: int
    total: int


class ResponseData(_ResponseOptionalData):
    result: B24APIResult
    time: TimeResponseData


class ListResponseData(TypedDict):
    result: JSONList
    time: TimeResponseData


class ListFastResponseData(TypedDict):
    result: JSONGenerator
    time: TimeResponseData


class BatchResultData(TypedDict):
    result: Union[Dict[Text, B24APIResult], List[B24APIResult]]
    result_error: Union[JSONDict, JSONList]
    result_total: Union[Dict[Text, int], List[int]]
    result_next: Union[Dict[Text, int], List[int]]
    result_time: Union[Dict[Text, TimeResponseData], List[TimeResponseData]]


class BatchResponseData(TypedDict):
    result: BatchResultData
    time: TimeResponseData


class B24AppInfoInstallData(TypedDict):
    installed: bool
    version: int
    status: Annotated[Text, B24AppStatusLiteral]
    scope: Text
    domain: Text
    uri: Text
    client_endpoint: Text
    member_id: Text
    member_type: Text


class B24AppInfoResultData(TypedDict):
    client_id: Text
    scope: Text
    expires: Text
    install: B24AppInfoInstallData
    user_id: int


class BitrixAppInfoResponseData(_ResponseOptionalData):
    result: B24AppInfoResultData
    time: TimeResponseData
