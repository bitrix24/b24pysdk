from typing import Dict, List, Text, Tuple
from unittest.mock import Mock

import pytest

from b24pysdk.api.requests.bitrix_api_request import BitrixAPIRequest
from b24pysdk.api.responses import BitrixAPIResponse, BitrixTimeResponse
from b24pysdk.utils.types import JSONDict
from tests.unit.examples import TOKEN_MOCK
from tests.unit.helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requests,
    pytest.mark.bitrix_api_request,
]


_REQUEST_CASE_1 = {
    "params": {"ID": 1, "select": ["ID", "NAME"]},
    "kwargs": {"key_1": "value_1", "key_2": 123},
    "expected_str": "<BitrixAPIRequest user.get(ID=1, select=['ID', 'NAME'])>",
}

_REQUEST_CASE_2 = {
    "params": {"FIELDS": {"TITLE": "New Lead"}},
    "kwargs": {"halt": True},
    "expected_str": "<BitrixAPIRequest crm.lead.add(FIELDS={'TITLE': 'New Lead'})>",
}

_REQUEST_CASE_3 = {
    "params": {},
    "kwargs": {},
    "expected_str": "<BitrixAPIRequest tasks.task.list()>",
}

_REQUEST_CASE_4 = {
    "params": None,
    "kwargs": {},
    "expected_str": "<BitrixAPIRequest user.get(None)>",
}

_INIT_TEST_DATA: List[
    Tuple[
        Text,
        JSONDict,
    ]
] = [
    ("user.get", _REQUEST_CASE_1),
    ("crm.lead.add", _REQUEST_CASE_2),
    ("tasks.task.list", _REQUEST_CASE_3),
    ("user.get", _REQUEST_CASE_4),
]

_RESPONSE_JSON: JSONDict = {
    "result": {"id": 1, "name": "Test User"},
    "time": {
        "start": 1672531200.0,
        "finish": 1672531205.0,
        "duration": 5.0,
        "processing": 0.1,
        "date_start": "2023-01-01T00:00:00+00:00",
        "date_finish": "2023-01-01T00:00:05+00:00",
    },
    "next": 50,
    "total": 100,
}


@pytest.mark.parametrize(("api_method", "request_case"), _INIT_TEST_DATA)
def test_initialization_and_properties_variants(
        api_method: Text,
    request_case: Dict,
):
    params = request_case["params"]
    kwargs = request_case["kwargs"]
    expected_str = request_case["expected_str"]

    obj = BitrixAPIRequest(
        bitrix_token=TOKEN_MOCK,
        api_method=api_method,
        params=params,
        **kwargs,
    )

    assert obj._bitrix_token is TOKEN_MOCK
    assert obj._api_method == api_method
    assert obj._params == params
    assert obj._kwargs == kwargs
    assert obj._response is None
    assert obj._as_tuple == (api_method, params)
    assert str(obj) == expected_str


def test_repr_contains_all_fields():
    obj = BitrixAPIRequest(
        bitrix_token=TOKEN_MOCK,
        api_method="test_method",
        params={"key": "value"},
    )

    repr_output = repr(obj)

    assert "BitrixAPIRequest(" in repr_output
    assert "bitrix_token=" in repr_output
    assert "api_method='test_method'" in repr_output
    assert "params={'key': 'value'}" in repr_output


def test_call_method_success():
    token_mock = Mock()
    token_mock.call_method.return_value = _RESPONSE_JSON

    obj = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="some.method",
        params=_REQUEST_CASE_1["params"],
        **_REQUEST_CASE_1["kwargs"],
    )

    response = obj.call()

    assert isinstance(response, BitrixAPIResponse)
    assert response.result == _RESPONSE_JSON["result"]
    assert obj._response is response

    token_mock.call_method.assert_called_once_with(
        api_method="some.method",
        params=_REQUEST_CASE_1["params"],
        **_REQUEST_CASE_1["kwargs"],
    )


def test_response_property_calls_call_if_not_set():
    token_mock = Mock()
    token_mock.call_method.return_value = _RESPONSE_JSON

    obj = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="test.call",
        params=None,
    )

    response = obj.response

    assert isinstance(response, BitrixAPIResponse)
    assert token_mock.call_method.call_count == 1

    response_2 = obj.response
    assert response_2 is response
    assert token_mock.call_method.call_count == 1


def test_result_and_time_properties_access():
    token_mock = Mock()
    token_mock.call_method.return_value = _RESPONSE_JSON

    obj = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="get.data",
        params=None,
    )

    result = obj.result
    time = obj.time

    assert result == _RESPONSE_JSON["result"]
    assert isinstance(time, BitrixTimeResponse)
    assert time.start == _RESPONSE_JSON["time"]["start"]
    assert token_mock.call_method.call_count == 1


def test_slots_defined():
    assert_slots(BitrixAPIRequest)
