import typing
from unittest.mock import Mock

from b24pysdk.bitrix_api.requests import BitrixAPIRequest
from b24pysdk.utils.types import JSONDict

__all__ = [
    "EXAMPLE_TIME_1",
    "EXAMPLE_TIME_2",
    "EXAMPLE_TIME_3",
    "INSTALL_DATA",
    "JSON_EMPTY_DICT",
    "JSON_EMPTY_LIST",
    "REQUESTS_MAP",
    "REQUESTS_SEQ",
    "REQ_1",
    "REQ_2",
    "RESPONSE_DICT",
    "TOKEN_MOCK",
]

TOKEN_MOCK: typing.Final[Mock] = Mock()
""""""

EXAMPLE_TIME_1: typing.Final[typing.Dict] = {
    "start": 1672531200.0,
    "finish": 1672531205.0,
    "duration": 5.0,
    "processing": 0.1,
    "date_start": "2023-01-01T00:00:00+00:00",
    "date_finish": "2023-01-01T00:00:05+00:00",
}
""""""

EXAMPLE_TIME_2: typing.Final[typing.Dict] = {
    "start": 1700000000.0,
    "finish": 1700000010.0,
    "duration": 10.0,
    "processing": 0.25,
    "date_start": "2023-11-14T22:13:20+00:00",
    "date_finish": "2023-11-14T22:13:30+00:00",
}
""""""

EXAMPLE_TIME_3: typing.Final[typing.Dict] = {
    "start": 1577836800.0,
    "finish": 1577836802.0,
    "duration": 2.0,
    "processing": 0.01,
    "date_start": "2020-01-01T00:00:00+00:00",
    "date_finish": "2020-01-01T00:00:02+00:00",
}
""""""

INSTALL_DATA: JSONDict = {
    "installed": True,
    "version": "2",
    "status": "P",
    "scope": "crm,user,task",
    "domain": "example.bitrix24.com",
    "uri": "https://example.bitrix24.com",
    "client_endpoint": "https://example.bitrix24.com/rest/",
    "member_id": "123456",
    "member_type": "user",
}
""""""

JSON_EMPTY_DICT: JSONDict = {
    "result": {},
    "result_error": {},
    "result_total": {},
    "result_next": {},
    "result_time": {},
}

JSON_EMPTY_LIST: JSONDict = {
    "result": [],
    "result_error": [],
    "result_total": [],
    "result_next": [],
    "result_time": [],
}

REQ_1: typing.Final[BitrixAPIRequest] = BitrixAPIRequest(
    bitrix_token=TOKEN_MOCK, api_method="user.get", params={"ID": 1},
)
""""""

REQ_2: typing.Final[BitrixAPIRequest] = BitrixAPIRequest(
    bitrix_token=TOKEN_MOCK, api_method="crm.lead.add", params={"FIELDS": {"TITLE": "New Lead"}},
)
""""""

REQUESTS_MAP: typing.Final[typing.Mapping[typing.Text, BitrixAPIRequest]] = {
    "user": REQ_1,
    "add_lead": REQ_2,
}
""""""

REQUESTS_SEQ: typing.Final[typing.List[BitrixAPIRequest]] = [REQ_1, REQ_2]
""""""

RESPONSE_DICT: typing.Final[JSONDict] = {
    "result": {
        "result": {"user": {"ID": 1}, "add_lead": 5},
        "result_error": {},
        "result_total": {"user": 1, "add_lead": 1},
        "result_next": {"user": None, "add_lead": None},
        "result_time": {"user": EXAMPLE_TIME_1, "add_lead": EXAMPLE_TIME_2},
    },
    "time": EXAMPLE_TIME_3,
}
""""""
