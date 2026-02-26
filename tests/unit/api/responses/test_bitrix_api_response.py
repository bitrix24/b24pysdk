import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.utils.types import JSONDict, JSONList
from tests.unit.examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2
from tests.unit.helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_response,
]


_JSON_DATA_WITH_NEXT_AND_TOTAL: JSONDict = {
    "result": {"id": 123, "name": "test"},
    "time": EXAMPLE_TIME_1,
    "next": 50,
    "total": 100,
}

_JSON_DATA_WITH_NEXT_ONLY: JSONDict = {
    "result": [1, 2, 3],
    "time": EXAMPLE_TIME_2,
    "next": 25,
    "total": None,
}

_JSON_DATA_WITH_TOTAL_ONLY: JSONDict = {
    "result": "success",
    "time": EXAMPLE_TIME_1,
    "next": None,
    "total": 50,
}

_JSON_DATA_WITHOUT_NEXT_AND_TOTAL: JSONDict = {
    "result": {"status": "ok"},
    "time": EXAMPLE_TIME_2,
    "next": None,
    "total": None,
}

_JSON_DATA_COMPLEX_RESULT: JSONDict = {
    "result": {
        "users": [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"},
        ],
        "count": 2,
    },
    "time": EXAMPLE_TIME_1,
    "next": 100,
    "total": 250,
}

_JSON_DATA_DIFFERENT_RESULT_TYPES: JSONDict = {
    "result": 42,
    "time": EXAMPLE_TIME_2,
    "next": None,
    "total": None,
}

_JSON_DATA_BOOLEAN_RESULT: JSONDict = {
    "result": True,
    "time": EXAMPLE_TIME_1,
    "next": 10,
    "total": 1,
}

_TEST_DATA: JSONList = [
    _JSON_DATA_WITH_NEXT_AND_TOTAL,
    _JSON_DATA_WITH_NEXT_ONLY,
    _JSON_DATA_WITH_TOTAL_ONLY,
    _JSON_DATA_WITHOUT_NEXT_AND_TOTAL,
    _JSON_DATA_COMPLEX_RESULT,
    _JSON_DATA_DIFFERENT_RESULT_TYPES,
    _JSON_DATA_BOOLEAN_RESULT,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = BitrixAPIResponse.from_dict(json_data)

    assert obj.result == json_data["result"]
    verify_time(obj.time, json_data["time"])
    assert obj.next == json_data.get("next")
    assert obj.total == json_data.get("total")


def test_frozen_instance():
    assert_frozen_instance(BitrixAPIResponse, _JSON_DATA_WITH_NEXT_AND_TOTAL, "result")


def test_equality_disabled():
    assert_equality_disabled(BitrixAPIResponse, _JSON_DATA_WITH_NEXT_AND_TOTAL)


def test_is_dataclass():
    assert_is_dataclass(BitrixAPIResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAPIResponse)
