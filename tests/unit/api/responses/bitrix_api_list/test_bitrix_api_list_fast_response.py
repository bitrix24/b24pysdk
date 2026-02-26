import pytest

from b24pysdk.api.responses import BitrixAPIListFastResponse
from b24pysdk.utils.types import JSONDict, JSONDictGenerator, JSONList
from tests.unit.examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, EXAMPLE_TIME_3
from tests.unit.helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_list,
    pytest.mark.bitrix_api_list_fast_response,
]


def _simple_generator() -> JSONDictGenerator:
    yield from [{"id": 1}, {"id": 2}, {"id": 3}]


def _empty_generator() -> JSONDictGenerator:
    yield from []


def _nested_generator() -> JSONDictGenerator:
    yield from [
        {"user": {"id": 1, "name": "John"}},
        {"user": {"id": 2, "name": "Jane"}},
    ]


def _mixed_generator() -> JSONDictGenerator:
    yield from [
        {"id": 1, "active": True},
        {"name": "test", "tags": ["tag1"]},
        {"data": None},
    ]


_JSON_DATA_SIMPLE: JSONDict = {
    "result": [{"id": 1}, {"id": 2}, {"id": 3}],
    "time": EXAMPLE_TIME_1,
}

_JSON_DATA_EMPTY: JSONDict = {
    "result": [],
    "time": EXAMPLE_TIME_2,
}

_JSON_DATA_NESTED: JSONDict = {
    "result": [
        {"user": {"id": 1, "name": "John"}},
        {"user": {"id": 2, "name": "Jane"}},
    ],
    "time": EXAMPLE_TIME_3,
}

_JSON_DATA_MIXED: JSONDict = {
    "result": [
        {"id": 1, "active": True},
        {"name": "test", "tags": ["tag1"]},
        {"data": None},
    ],
    "time": EXAMPLE_TIME_1,
}

_TEST_DATA: JSONList = [
    _JSON_DATA_SIMPLE,
    _JSON_DATA_EMPTY,
    _JSON_DATA_NESTED,
    _JSON_DATA_MIXED,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = BitrixAPIListFastResponse.from_dict(json_data)

    result_list = list(obj.result)
    expected_list = json_data["result"]

    assert result_list == expected_list
    assert isinstance(obj.result, list)

    verify_time(obj.time, json_data["time"])


def test_time_property_creates_new_instance():
    json_data: JSONDict = {
        "result": [{"id": 1}],
        "time": EXAMPLE_TIME_1,
    }
    obj = BitrixAPIListFastResponse.from_dict(json_data)

    time_obj_1 = obj.time
    time_obj_2 = obj.time

    assert time_obj_1 is not time_obj_2
    assert time_obj_1.start == time_obj_2.start
    assert time_obj_1.finish == time_obj_2.finish


def test_frozen_instance():
    assert_frozen_instance(BitrixAPIListFastResponse, _JSON_DATA_SIMPLE, "result")


def test_equality_disabled():
    assert_equality_disabled(BitrixAPIListFastResponse, _JSON_DATA_SIMPLE)


def test_is_dataclass():
    assert_is_dataclass(BitrixAPIListFastResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAPIListFastResponse)
