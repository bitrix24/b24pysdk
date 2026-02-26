from typing import Dict, List
from unittest.mock import Mock

import pytest

from b24pysdk.api.requests.bitrix_api_list_request import BitrixAPIListFastRequest
from b24pysdk.api.requests.bitrix_api_request import BitrixAPIRequest
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixTimeResponse
from b24pysdk.utils.types import JSONDict
from tests.unit.examples import EXAMPLE_TIME_1, TOKEN_MOCK
from tests.unit.helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requests,
    pytest.mark.bitrix_api_list_fast_request,
]


_LIST_FAST_CASE_1 = {
    "params": {"filter": {"ID": 1}},
    "api_method": "crm.deal.list",
    "descending": True,
    "limit": 1000,
    "kwargs": {"extra_opt": "value"},
}

_LIST_FAST_CASE_2 = {
    "params": None,
    "api_method": "user.get",
    "descending": False,
    "limit": None,
    "kwargs": {},
}

_LIST_FAST_TEST_DATA: List[Dict] = [
    _LIST_FAST_CASE_1,
    _LIST_FAST_CASE_2,
]

_RESPONSE_JSON: JSONDict = {
    "result": {"items": [{"id": 1}], "meta": {}},
    "time": EXAMPLE_TIME_1,
    "next": 50,
    "total": 100,
}


@pytest.mark.parametrize("request_case", _LIST_FAST_TEST_DATA)
def test_initialization_and_properties_variants(request_case: Dict):
    base_request = BitrixAPIRequest(
        bitrix_token=TOKEN_MOCK,
        api_method=request_case["api_method"],
        params=request_case["params"],
    )

    obj = BitrixAPIListFastRequest(
        bitrix_api_request=base_request,
        descending=request_case["descending"],
        limit=request_case["limit"],
        **request_case["kwargs"],
    )

    assert obj._bitrix_token is base_request._bitrix_token
    assert obj._api_method == base_request._api_method
    assert obj._params == base_request._params
    assert obj._descending == request_case["descending"]
    assert obj._limit == request_case["limit"]

    for key, value in request_case["kwargs"].items():
        assert obj._kwargs[key] == value


def test_call_method_success():
    token_mock = Mock()
    token_mock.call_list_fast.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="crm.company.list",
        params=_LIST_FAST_CASE_1["params"],
    )

    obj = BitrixAPIListFastRequest(
        bitrix_api_request=base_req,
        descending=_LIST_FAST_CASE_1["descending"],
        limit=500,
        **_LIST_FAST_CASE_1["kwargs"],
    )

    response = obj.call()

    assert isinstance(response, BitrixAPIListFastResponse)
    assert response.result == _RESPONSE_JSON["result"]
    assert obj._response is response

    token_mock.call_list_fast.assert_called_once_with(
        api_method="crm.company.list",
        params=_LIST_FAST_CASE_1["params"],
        descending=_LIST_FAST_CASE_1["descending"],
        limit=500,
        **_LIST_FAST_CASE_1["kwargs"],
    )


def test_response_property_calls_call_if_not_set():
    token_mock = Mock()
    token_mock.call_list_fast.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="lists.element.get",
        params=None,
    )

    obj = BitrixAPIListFastRequest(
        bitrix_api_request=base_req,
        descending=False,
    )

    response = obj.response

    assert isinstance(response, BitrixAPIListFastResponse)
    assert token_mock.call_list_fast.call_count == 1

    response_2 = obj.response
    assert response_2 is response
    assert token_mock.call_list_fast.call_count == 1


def test_result_and_time_properties_access():
    token_mock = Mock()
    token_mock.call_list_fast.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="tasks.task.list",
        params=None,
    )

    obj = BitrixAPIListFastRequest(
        bitrix_api_request=base_req,
    )

    result = obj.result

    assert result == _RESPONSE_JSON["result"]
    assert isinstance(obj.response.time, BitrixTimeResponse)
    assert token_mock.call_list_fast.call_count == 1


def test_slots_defined():
    assert_slots(BitrixAPIListFastRequest)
