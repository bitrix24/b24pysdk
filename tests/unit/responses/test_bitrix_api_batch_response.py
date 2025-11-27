import pytest

from b24pysdk.bitrix_api.responses import B24APIBatchResult, BitrixAPIBatchResponse

pytestmark = [
    pytest.mark.unit,
    pytest.mark.bitrix_api_batch_response,
]


def _make_time_response_dict():
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


def _make_batch_response_dict_with_dict_result():
    time_resp = _make_time_response_dict()
    return {
        "result": {
            "result": {"cmd1": {"id": 123}, "cmd2": {"id": 456}},
            "result_error": {},
            "result_total": {"cmd1": 1, "cmd2": 1},
            "result_next": {},
            "result_time": {
                "cmd1": time_resp,
                "cmd2": time_resp,
            },
        },
        "time": time_resp,
    }


def _make_batch_response_dict_with_list_result():
    time_resp = _make_time_response_dict()
    return {
        "result": {
            "result": [{"id": 123}, {"id": 456}],
            "result_error": [],
            "result_total": [1, 1],
            "result_next": [],
            "result_time": [time_resp, time_resp],
        },
        "time": time_resp,
    }


def test_b24api_batch_result_from_dict_with_dict():
    time_resp = _make_time_response_dict()
    input_data = {
        "result": {"cmd1": {"id": 123}},
        "result_error": {},
        "result_total": {"cmd1": 1},
        "result_next": {},
        "result_time": {"cmd1": time_resp},
    }

    obj = B24APIBatchResult.from_dict(input_data)

    assert obj.result == input_data["result"]
    assert obj.result_error == input_data["result_error"]
    assert obj.result_total == input_data["result_total"]
    assert obj.result_next == input_data["result_next"]
    assert isinstance(obj.result_time, dict)
    assert len(obj.result_time) == 1
    assert obj.result_time["cmd1"].start == time_resp["start"]
    assert obj.result_time["cmd1"].operating == time_resp["operating"]


def test_b24api_batch_result_from_dict_with_list():
    time_resp = _make_time_response_dict()
    input_data = {
        "result": [{"id": 123}],
        "result_error": [],
        "result_total": [1],
        "result_next": [],
        "result_time": [time_resp],
    }

    obj = B24APIBatchResult.from_dict(input_data)

    assert obj.result == input_data["result"]
    assert obj.result_error == input_data["result_error"]
    assert obj.result_total == input_data["result_total"]
    assert obj.result_next == input_data["result_next"]
    assert isinstance(obj.result_time, list)
    assert len(obj.result_time) == 1
    assert obj.result_time[0].start == time_resp["start"]
    assert obj.result_time[0].operating == time_resp["operating"]


def test_b24api_batch_result_to_dict_roundtrip_dict():
    time_resp = _make_time_response_dict()
    input_data = {
        "result": {"cmd1": {"id": 123}},
        "result_error": {"cmd2": "error"},
        "result_total": {"cmd1": 1},
        "result_next": {"cmd1": 50},
        "result_time": {"cmd1": time_resp},
    }

    obj = B24APIBatchResult.from_dict(input_data)
    output_dict = obj.to_dict()

    assert output_dict["result"] == input_data["result"]
    assert output_dict["result_error"] == input_data["result_error"]
    assert output_dict["result_total"] == input_data["result_total"]
    assert output_dict["result_next"] == input_data["result_next"]
    assert isinstance(output_dict["result_time"], dict)
    assert output_dict["result_time"]["cmd1"]["start"] == time_resp["start"]


def test_b24api_batch_result_to_dict_roundtrip_list():
    time_resp = _make_time_response_dict()
    input_data = {
        "result": [{"id": 123}],
        "result_error": ["error1"],
        "result_total": [1],
        "result_next": [10],
        "result_time": [time_resp],
    }

    obj = B24APIBatchResult.from_dict(input_data)
    output_dict = obj.to_dict()

    assert output_dict["result"] == input_data["result"]
    assert output_dict["result_error"] == input_data["result_error"]
    assert output_dict["result_total"] == input_data["result_total"]
    assert output_dict["result_next"] == input_data["result_next"]
    assert isinstance(output_dict["result_time"], list)
    assert output_dict["result_time"][0]["start"] == time_resp["start"]


def test_bitrix_api_batch_response_from_dict_with_dict_result():
    batch_dict = _make_batch_response_dict_with_dict_result()
    obj = BitrixAPIBatchResponse.from_dict(batch_dict)

    inner = batch_dict["result"]
    assert obj.result.result == inner["result"]
    assert obj.result.result_error == inner["result_error"]
    assert obj.result.result_total == inner["result_total"]
    assert obj.result.result_next == inner["result_next"]
    assert isinstance(obj.result.result_time, dict)
    assert obj.result.result_time["cmd1"].start == inner["result_time"]["cmd1"]["start"]

    assert obj.time.start == batch_dict["time"]["start"]
    assert obj.time.operating == batch_dict["time"]["operating"]


def test_bitrix_api_batch_response_from_dict_with_list_result():
    batch_dict = _make_batch_response_dict_with_list_result()
    obj = BitrixAPIBatchResponse.from_dict(batch_dict)

    inner = batch_dict["result"]
    assert obj.result.result == inner["result"]
    assert obj.result.result_error == inner["result_error"]
    assert obj.result.result_total == inner["result_total"]
    assert obj.result.result_next == inner["result_next"]
    assert isinstance(obj.result.result_time, list)
    assert obj.result.result_time[0].start == inner["result_time"][0]["start"]

    assert obj.time.start == batch_dict["time"]["start"]


def test_bitrix_api_batch_response_frozen():
    batch_dict = _make_batch_response_dict_with_dict_result()
    obj = BitrixAPIBatchResponse.from_dict(batch_dict)
    with pytest.raises(AttributeError):
        obj.result = None


def test_bitrix_api_batch_response_equality_disabled():
    batch_dict = _make_batch_response_dict_with_dict_result()
    obj1 = BitrixAPIBatchResponse.from_dict(batch_dict)
    obj2 = BitrixAPIBatchResponse.from_dict(batch_dict)
    assert obj1 is not obj2
    assert obj1 != obj2


def test_bitrix_api_batch_response_repr():
    batch_dict = _make_batch_response_dict_with_dict_result()
    obj = BitrixAPIBatchResponse.from_dict(batch_dict)
    repr_str = repr(obj)
    assert "BitrixAPIBatchResponse" in repr_str
    assert "B24APIBatchResult" in repr_str
    assert "time=" in repr_str
