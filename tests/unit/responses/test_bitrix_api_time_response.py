from datetime import datetime, timezone

import pytest

from b24pysdk.bitrix_api.responses import BitrixAPITimeResponse

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bitrix_api_time_response,
]


def make_sample_json_response():
    return {
        "start": 1672531200.0,
        "finish": 1672531205.0,
        "duration": 5.0,
        "processing": 0.1,
        "date_start": "2023-01-01T00:00:00+00:00",
        "date_finish": "2023-01-01T00:00:05+00:00",
        "operating_reset_at": 1672617600,
        "operating": 0.8,
    }


def make_sample_json_response_no_optional():
    return {
        "start": 1672531200.0,
        "finish": 1672531205.0,
        "duration": 5.0,
        "processing": 0.1,
        "date_start": "2023-01-01T00:00:00+00:00",
        "date_finish": "2023-01-01T00:00:05+00:00",
    }


def test_from_dict_with_all_fields():
    data = make_sample_json_response()
    obj = BitrixAPITimeResponse.from_dict(data)

    assert obj.start == data["start"]
    assert obj.finish == data["finish"]
    assert obj.duration == data["duration"]
    assert obj.processing == data["processing"]
    assert obj.date_start == datetime.fromisoformat(data["date_start"])
    assert obj.date_finish == datetime.fromisoformat(data["date_finish"])
    assert obj.operating_reset_at == datetime.fromtimestamp(data["operating_reset_at"], tz=timezone.utc)
    assert obj.operating == data["operating"]


def test_from_dict_without_optional_fields():
    data = make_sample_json_response_no_optional()
    obj = BitrixAPITimeResponse.from_dict(data)

    assert obj.operating_reset_at is None
    assert obj.operating is None


def test_to_dict_roundtrip():
    data = make_sample_json_response()
    obj = BitrixAPITimeResponse.from_dict(data)
    result_dict = obj.to_dict()

    expected_dict = {
        "start": data["start"],
        "finish": data["finish"],
        "duration": data["duration"],
        "processing": data["processing"],
        "date_start": datetime.fromisoformat(data["date_start"]),
        "date_finish": datetime.fromisoformat(data["date_finish"]),
        "operating_reset_at": datetime.fromtimestamp(data["operating_reset_at"], tz=timezone.utc),
        "operating": data["operating"],
    }

    assert result_dict == expected_dict


def test_frozen_instance():
    data = make_sample_json_response()
    obj = BitrixAPITimeResponse.from_dict(data)
    with pytest.raises(AttributeError):
        obj.start = 0.0


def test_equality_disabled():
    data = make_sample_json_response()
    obj1 = BitrixAPITimeResponse.from_dict(data)
    obj2 = BitrixAPITimeResponse.from_dict(data)
    assert obj1 is not obj2
    assert obj1 != obj2
