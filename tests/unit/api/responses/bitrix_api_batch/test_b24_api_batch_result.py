import pytest

from b24pysdk.api.responses import B24APIBatchResult
from b24pysdk.utils.types import JSONDict, JSONList
from tests.unit.examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, EXAMPLE_TIME_3, JSON_EMPTY_DICT, JSON_EMPTY_LIST
from tests.unit.helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_batch,
    pytest.mark.b24_api_batch_result,
]


_JSON_DICT: JSONDict = {
    "result": {"user.get": {"result": {"id": 123}}},
    "result_error": {"user.get": {}},
    "result_total": {"user.get": 1},
    "result_next": {},
    "result_time": {"user.get": EXAMPLE_TIME_1},
}

_JSON_LIST: JSONDict = {
    "result": [{"id": 1}, {"name": "ok"}],
    "result_error": [],
    "result_total": [1, 0],
    "result_next": [],
    "result_time": [EXAMPLE_TIME_2, EXAMPLE_TIME_3],
}

_TEST_DATA: JSONList = [
    _JSON_DICT,
    _JSON_LIST,
    JSON_EMPTY_DICT,
    JSON_EMPTY_LIST,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = B24APIBatchResult.from_dict(json_data)

    assert obj.result == json_data["result"]
    assert obj.result_error == json_data["result_error"]
    assert obj.result_total == json_data["result_total"]
    assert obj.result_next == json_data["result_next"]

    raw_time = json_data["result_time"]
    parsed_time = obj.result_time

    if isinstance(raw_time, dict):
        assert isinstance(parsed_time, dict)
        assert set(parsed_time.keys()) == set(raw_time.keys())

        for k in raw_time:
            verify_time(parsed_time[k], raw_time[k])

    elif isinstance(raw_time, list):
        assert isinstance(parsed_time, list)
        assert len(parsed_time) == len(raw_time)

        for i in range(len(raw_time)):
            verify_time(parsed_time[i], raw_time[i])

    else:
        raise TypeError("Unexpected type for result_time")


def test_frozen_instance():
    assert_frozen_instance(B24APIBatchResult, _JSON_DICT, "result")


def test_equality_disabled():
    assert_equality_disabled(B24APIBatchResult, _JSON_DICT)


def test_is_dataclass():
    assert_is_dataclass(B24APIBatchResult)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(B24APIBatchResult)
