from datetime import datetime, timezone
from typing import List, Optional, Tuple

import pytest

from b24pysdk.bitrix_api.responses import BitrixAPITimeResponse
from b24pysdk.utils.types import JSONDict

from ..examples import EXAMPLE_TIME_1
from ..helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_api_time_response,
]

_JSON_DATA_FULL: JSONDict = {
    "start": 1672531200.0,
    "finish": 1672531205.0,
    "duration": 5.0,
    "processing": 0.1,
    "date_start": "2023-01-01T00:00:00+00:00",
    "date_finish": "2023-01-01T00:00:05+00:00",
    "operating_reset_at": 1672617600,
    "operating": 0.8,
}

_JSON_DATA_ANOTHER_FULL: JSONDict = {
    "start": 1700000000.0,
    "finish": 1700000010.0,
    "duration": 10.0,
    "processing": 0.25,
    "date_start": "2023-11-14T22:13:20+00:00",
    "date_finish": "2023-11-14T22:13:30+00:00",
    "operating_reset_at": 1700086400.0,
    "operating": 0.95,
}

_JSON_DATA_ONLY_RESET_AT: JSONDict = {
    "start": 1609459200,
    "finish": 1609459260,
    "duration": 60,
    "processing": 0.05,
    "date_start": "2021-01-01T00:00:00+00:00",
    "date_finish": "2021-01-01T00:01:00+00:00",
    "operating_reset_at": 1609545600,
}

_JSON_DATA_ONLY_OPERATING: JSONDict = {
    "start": 1577836800.0,
    "finish": 1577836802.0,
    "duration": 2.0,
    "processing": 0.01,
    "date_start": "2020-01-01T00:00:00+00:00",
    "date_finish": "2020-01-01T00:00:02+00:00",
    "operating": 0.6,
}

_TEST_DATA: List[Tuple[JSONDict, Optional[datetime], Optional[float]]] = [
    (
        _JSON_DATA_FULL,
        datetime.fromtimestamp(1672617600, tz=timezone.utc),
        0.8,
    ),
    (
        EXAMPLE_TIME_1,
        None,
        None,
    ),
    (
        _JSON_DATA_ANOTHER_FULL,
        datetime.fromtimestamp(1700086400.0, tz=timezone.utc),
        0.95,
    ),
    (
        _JSON_DATA_ONLY_RESET_AT,
        datetime.fromtimestamp(1609545600, tz=timezone.utc),
        None,
    ),
    (
        _JSON_DATA_ONLY_OPERATING,
        None,
        0.6,
    ),
]


@pytest.mark.parametrize(("json_data", "expected_operating_reset_at", "expected_operating"), _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict, expected_operating_reset_at: Optional[datetime], expected_operating: Optional[float]):
    obj = BitrixAPITimeResponse.from_dict(json_data)

    assert obj.start == json_data["start"]
    assert obj.finish == json_data["finish"]
    assert obj.duration == json_data["duration"]
    assert obj.processing == json_data["processing"]
    assert obj.date_start == datetime.fromisoformat(json_data["date_start"])
    assert obj.date_finish == datetime.fromisoformat(json_data["date_finish"])
    assert obj.operating_reset_at == expected_operating_reset_at
    assert obj.operating == expected_operating


def test_frozen_instance():
    assert_frozen_instance(BitrixAPITimeResponse, EXAMPLE_TIME_1, "start")


def test_equality_disabled():
    assert_equality_disabled(BitrixAPITimeResponse, EXAMPLE_TIME_1)


def test_is_dataclass():
    assert_is_dataclass(BitrixAPITimeResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAPITimeResponse)
