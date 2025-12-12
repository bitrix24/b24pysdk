import pytest

from b24pysdk.bitrix_api.responses import BitrixAPIBatchResponse
from b24pysdk.utils.types import JSONDict, JSONList

from ...examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, EXAMPLE_TIME_3, JSON_EMPTY_DICT, JSON_EMPTY_LIST
from ...helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_batch,
    pytest.mark.bitrix_api_batch_response,
]


_RESULT_DICT_CASE: JSONDict = {
    "result": {"user.get": {"result": {"id": 123}}},
    "result_error": {},
    "result_total": {},
    "result_next": {},
    "result_time": {"user.get": EXAMPLE_TIME_1},
}

_RESULT_LIST_CASE: JSONDict = {
    "result": [{"id": 1}, {"name": "test"}],
    "result_error": [],
    "result_total": [],
    "result_next": [],
    "result_time": [EXAMPLE_TIME_2, EXAMPLE_TIME_3],
}

_RESPONSE_DICT: JSONDict = {
    "result": _RESULT_DICT_CASE,
    "time": EXAMPLE_TIME_1,
}

_RESPONSE_LIST: JSONDict = {
    "result": _RESULT_LIST_CASE,
    "time": EXAMPLE_TIME_2,
}

_RESPONSE_EMPTY_DICT: JSONDict = {
    "result": JSON_EMPTY_DICT,
    "time": EXAMPLE_TIME_3,
}

_RESPONSE_EMPTY_LIST: JSONDict = {
    "result": JSON_EMPTY_LIST,
    "time": EXAMPLE_TIME_1,
}

_TEST_DATA: JSONList = [
    _RESPONSE_DICT,
    _RESPONSE_LIST,
    _RESPONSE_EMPTY_DICT,
    _RESPONSE_EMPTY_LIST,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = BitrixAPIBatchResponse.from_dict(json_data)

    result_data = json_data["result"]
    result_obj = obj.result

    assert result_obj.result == result_data["result"]
    assert result_obj.result_error == result_data["result_error"]
    assert result_obj.result_total == result_data["result_total"]
    assert result_obj.result_next == result_data["result_next"]

    raw_result_time = result_data["result_time"]
    parsed_result_time = result_obj.result_time

    if isinstance(raw_result_time, dict):
        assert isinstance(parsed_result_time, dict)
        assert parsed_result_time.keys() == raw_result_time.keys()

        for key in raw_result_time:
            verify_time(parsed_result_time[key], raw_result_time[key])

    elif isinstance(raw_result_time, list):
        assert isinstance(parsed_result_time, list)
        assert len(parsed_result_time) == len(raw_result_time)

        for i, time_item in enumerate(raw_result_time):
            verify_time(parsed_result_time[i], time_item)

    else:
        raise TypeError("Unexpected result_time type")

    verify_time(obj.time, json_data["time"])
    assert obj.next is None
    assert obj.total is None


def test_frozen_instance():
    assert_frozen_instance(BitrixAPIBatchResponse, _RESPONSE_DICT, "result")


def test_equality_disabled():
    assert_equality_disabled(BitrixAPIBatchResponse, _RESPONSE_DICT)


def test_is_dataclass():
    assert_is_dataclass(BitrixAPIBatchResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAPIBatchResponse)
