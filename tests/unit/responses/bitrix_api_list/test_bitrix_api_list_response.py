import pytest

from b24pysdk.bitrix_api.responses import BitrixAPIListResponse
from b24pysdk.utils.types import JSONDict, JSONList

from ...examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, EXAMPLE_TIME_3
from ...helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_list,
    pytest.mark.bitrix_api_list_response,
]


_JSON_DATA_SIMPLE_LIST: JSONDict = {
    "result": [{"id": 1}, {"id": 2}, {"id": 3}],
    "time": EXAMPLE_TIME_1,
}

_JSON_DATA_EMPTY_LIST: JSONDict = {
    "result": [],
    "time": EXAMPLE_TIME_2,
}

_JSON_DATA_NESTED_OBJECTS: JSONDict = {
    "result": [
        {"user": {"id": 1, "name": "John", "email": "john@test.com"}},
        {"user": {"id": 2, "name": "Jane", "email": "jane@test.com"}},
    ],
    "time": EXAMPLE_TIME_3,
}

_JSON_DATA_MIXED_TYPES: JSONDict = {
    "result": [
        {"id": 1, "active": True, "score": 95.5},
        {"name": "test", "tags": ["tag1", "tag2"], "metadata": {"created": "2023-01-01"}},
        {"data": None, "count": 0},
    ],
    "time": EXAMPLE_TIME_1,
}

_JSON_DATA_LARGE_LIST: JSONDict = {
    "result": [{"item": i, "value": f"value_{i}"} for i in range(10)],
    "time": EXAMPLE_TIME_2,
}

_JSON_DATA_WITH_SPECIAL_VALUES: JSONDict = {
    "result": [
        {"empty_string": "", "zero": 0, "null_value": None},
        {"list": [], "dict": {}},
        {"boolean": False, "negative": -1},
    ],
    "time": EXAMPLE_TIME_3,
}

_JSON_DATA_SINGLE_ITEM: JSONDict = {
    "result": [{"id": 42, "name": "single_item"}],
    "time": EXAMPLE_TIME_1,
}

_JSON_DATA_COMPLEX_NESTING: JSONDict = {
    "result": [
        {
            "id": 1,
            "users": [
                {"name": "Alice", "roles": ["admin", "user"]},
                {"name": "Bob", "roles": ["user"]},
            ],
            "settings": {"theme": "dark", "notifications": True},
        },
    ],
    "time": EXAMPLE_TIME_2,
}

_TEST_DATA: JSONList = [
    _JSON_DATA_SIMPLE_LIST,
    _JSON_DATA_EMPTY_LIST,
    _JSON_DATA_NESTED_OBJECTS,
    _JSON_DATA_MIXED_TYPES,
    _JSON_DATA_LARGE_LIST,
    _JSON_DATA_WITH_SPECIAL_VALUES,
    _JSON_DATA_SINGLE_ITEM,
    _JSON_DATA_COMPLEX_NESTING,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = BitrixAPIListResponse.from_dict(json_data)

    assert obj.result == json_data["result"]
    assert isinstance(obj.result, list)

    verify_time(obj.time, json_data["time"])

    assert obj.next is None
    assert obj.total is None


def test_frozen_instance():
    assert_frozen_instance(BitrixAPIListResponse, _JSON_DATA_SIMPLE_LIST, "result")


def test_equality_disabled():
    assert_equality_disabled(BitrixAPIListResponse, _JSON_DATA_SIMPLE_LIST)


def test_is_dataclass():
    assert_is_dataclass(BitrixAPIListResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAPIListResponse)
