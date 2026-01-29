from typing import Dict, List, Text, Tuple
from unittest.mock import Mock

import pytest

from b24pysdk.bitrix_api.requests.bitrix_api_list_request import BitrixAPIListRequest
from b24pysdk.bitrix_api.requests.bitrix_api_request import BitrixAPIRequest
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPITimeResponse
from b24pysdk.utils.types import JSONDict

from ...examples import EXAMPLE_TIME_1, TOKEN_MOCK
from ...helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requests,
    pytest.mark.bitrix_api_list_request,
]


_LIST_REQUEST_CASE_1: JSONDict = {
    "params": {"filter": {"ID": 1}},
    "api_method": "crm.deal.list",
    "limit": 50,
    "kwargs": {"extra_opt": True},
    "expected_repr_substring": "limit=50",
}

_LIST_REQUEST_CASE_2: JSONDict = {
    "params": None,
    "api_method": "user.get",
    "limit": None,
    "kwargs": {},
    "expected_repr_substring": "limit=None",
}

_LIST_TEST_DATA: List[Tuple[Dict, Text]] = [
    (_LIST_REQUEST_CASE_1, _LIST_REQUEST_CASE_1["expected_repr_substring"]),
    (_LIST_REQUEST_CASE_2, _LIST_REQUEST_CASE_2["expected_repr_substring"]),
]

_RESPONSE_JSON: JSONDict = {
    "result": [{"id": 1, "title": "Deal 1"}, {"id": 2, "title": "Deal 2"}],
    "time": EXAMPLE_TIME_1,
    "next": 50,
    "total": 100,
}


@pytest.mark.parametrize(("request_case", "expected_repr_substring"), _LIST_TEST_DATA)
def test_initialization_and_properties_variants(
        request_case: Dict,
        expected_repr_substring: Text,
):
    base_request = BitrixAPIRequest(
        bitrix_token=TOKEN_MOCK,
        api_method=request_case["api_method"],
        params=request_case["params"],
    )

    obj = BitrixAPIListRequest(
        bitrix_api_request=base_request,
        limit=request_case["limit"],
        **request_case["kwargs"],
    )

    assert obj._bitrix_token is base_request._bitrix_token
    assert obj._api_method == base_request._api_method
    assert obj._params == base_request._params
    assert obj._limit == request_case["limit"]
    assert expected_repr_substring in repr(obj)

    for key, value in request_case["kwargs"].items():
        assert obj._kwargs[key] == value


def test_call_method_success():
    token_mock = Mock()
    token_mock.call_list.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="crm.company.list",
        params=_LIST_REQUEST_CASE_1["params"],
    )

    obj = BitrixAPIListRequest(
        bitrix_api_request=base_req,
        limit=_LIST_REQUEST_CASE_1["limit"],
        **_LIST_REQUEST_CASE_1["kwargs"],
    )

    response = obj.call()

    assert isinstance(response, BitrixAPIListResponse)
    assert response.result == _RESPONSE_JSON["result"]
    assert obj._response is response

    token_mock.call_list.assert_called_once_with(
        api_method="crm.company.list",
        params=_LIST_REQUEST_CASE_1["params"],
        limit=_LIST_REQUEST_CASE_1["limit"],
        **_LIST_REQUEST_CASE_1["kwargs"],
    )


def test_response_property_calls_call_if_not_set():
    token_mock = Mock()
    token_mock.call_list.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="lists.get",
        params=None,
    )

    obj = BitrixAPIListRequest(
        bitrix_api_request=base_req,
        limit=50,
    )

    response = obj.response

    assert isinstance(response, BitrixAPIListResponse)
    assert token_mock.call_list.call_count == 1

    response_2 = obj.response
    assert response_2 is response
    assert token_mock.call_list.call_count == 1


def test_result_and_time_properties_access():
    token_mock = Mock()
    token_mock.call_list.return_value = _RESPONSE_JSON

    base_req = BitrixAPIRequest(
        bitrix_token=token_mock,
        api_method="tasks.task.list",
        params=None,
    )

    obj = BitrixAPIListRequest(
        bitrix_api_request=base_req,
        limit=10,
    )

    result = obj.result

    assert result == _RESPONSE_JSON["result"]
    assert isinstance(obj.response.time, BitrixAPITimeResponse)
    assert token_mock.call_list.call_count == 1


def test_slots_defined():
    assert_slots(BitrixAPIListRequest)
