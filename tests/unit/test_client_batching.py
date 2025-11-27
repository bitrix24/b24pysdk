from typing import Any, Dict

from b24pysdk import Client
from b24pysdk.bitrix_api.requests import BitrixAPIRequest


def make_time() -> Dict[str, Any]:
    return {
        "start": 0.0,
        "finish": 0.1,
        "duration": 0.1,
        "processing": 0.05,
        "date_start": "2024-01-01T00:00:00+00:00",
        "date_finish": "2024-01-01T00:00:00+00:00",
    }


class DummyToken:
    def __init__(self):
        self.batch_calls = []
        self.batches_calls = []

    def call_batch(self, methods, *, halt=False, ignore_size_limit=False, timeout=None):
        self.batch_calls.append({
            "methods": methods,
            "halt": halt,
            "ignore_size_limit": ignore_size_limit,
            "timeout": timeout,
        })
        # Minimal valid batch JSON
        # Normalize result structure depending on mapping/sequence
        if isinstance(methods, dict):
            result = {key: {} for key in methods}
            result_error = dict.fromkeys(methods.keys())
            result_total = dict.fromkeys(methods.keys(), 0)
            result_next = dict.fromkeys(methods.keys(), 0)
            result_time = {key: make_time() for key in methods}
        else:
            n = len(methods)
            result = [{} for _ in range(n)]
            result_error = [None for _ in range(n)]
            result_total = [0 for _ in range(n)]
            result_next = [0 for _ in range(n)]
            result_time = [make_time() for _ in range(n)]

        return {
            "result": {
                "result": result,
                "result_error": result_error,
                "result_total": result_total,
                "result_next": result_next,
                "result_time": result_time,
            },
            "time": make_time(),
        }

    def call_batches(self, methods, *, halt=False, timeout=None):
        self.batches_calls.append({
            "methods": methods,
            "halt": halt,
            "timeout": timeout,
        })
        return {
            "result": {
                "result": [],
                "result_error": [],
                "result_total": [],
                "result_next": [],
                "result_time": [],
            },
            "time": make_time(),
        }


def test_client_call_batch_with_mapping():
    token = DummyToken()
    client = Client(token)

    r1 = BitrixAPIRequest(bitrix_token=token, api_method="crm.deal.get", params={"bitrix_id": 1})
    r2 = BitrixAPIRequest(bitrix_token=token, api_method="crm.deal.get", params={"bitrix_id": 2})

    batch = client.call_batch({"d1": r1, "d2": r2})
    _ = batch.result  # triggers call
    assert token.batch_calls, "call_batch should be invoked"


def test_client_call_batches_with_sequence():
    token = DummyToken()
    client = Client(token)

    r1 = BitrixAPIRequest(bitrix_token=token, api_method="crm.deal.get", params={"bitrix_id": 1})
    r2 = BitrixAPIRequest(bitrix_token=token, api_method="crm.deal.get", params={"bitrix_id": 2})

    batches = client.call_batches([r1, r2])
    _ = batches.result  # triggers call
    assert token.batches_calls, "call_batches should be invoked"
