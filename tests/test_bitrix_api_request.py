from typing import Any, Dict

from b24pysdk.bitrix_api.classes.request.bitrix_api_request import BitrixAPIRequest


class DummyToken:
    def __init__(self, response: Dict[str, Any]):
        self._response = response
        self.calls = []

    def call_method(self, api_method, params=None, *, timeout=None, **kwargs):
        self.calls.append((api_method, params, timeout, kwargs))
        return self._response


def make_json_response(result: Any) -> Dict[str, Any]:
    return {
        "result": result,
        "time": {
            "start": 0.0,
            "finish": 0.1,
            "duration": 0.1,
            "processing": 0.05,
            "date_start": "2024-01-01T00:00:00+00:00",
            "date_finish": "2024-01-01T00:00:00+00:00",
        },
    }


def test_bitrix_api_request_deferred_call_and_result():
    token = DummyToken(make_json_response({"a": 1}))
    req = BitrixAPIRequest(bitrix_token=token, api_method="crm.deal.get", params={"bitrix_id": 1})

    # Deferred: not called until result/time accessed
    assert token.calls == []

    # Access result triggers call
    assert req.result == {"a": 1}
    assert len(token.calls) == 1

    # Accessing time uses cached response, no extra call
    _ = req.time
    assert len(token.calls) == 1

    # __str__ contains method and params
    s = str(req)
    assert "crm.deal.get" in s
    assert "bitrix_id=1" in s
