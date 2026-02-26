from typing import Dict, List, Mapping, Sequence, Text, Tuple, Union
from unittest.mock import Mock

import pytest

from b24pysdk.api.requests.bitrix_api_batch_request import BitrixAPIBatchesRequest
from b24pysdk.api.requests.bitrix_api_request import BitrixAPIRequest
from b24pysdk.api.responses import BitrixAPIBatchResponse
from b24pysdk.credentials import AbstractBitrixToken
from b24pysdk.utils.types import JSONDict
from tests.unit.examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, EXAMPLE_TIME_3, REQUESTS_MAP, REQUESTS_SEQ, RESPONSE_DICT, TOKEN_MOCK
from tests.unit.helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requests,
    pytest.mark.bitrix_api_batches_request,
]


_RESPONSE_LIST: JSONDict = {
    "result": {
        "result": [{"ID": 1}, 5],
        "result_error": [],
        "result_total": [],
        "result_next": [],
        "result_time": [EXAMPLE_TIME_1, EXAMPLE_TIME_2],
    },
    "time": EXAMPLE_TIME_3,
}

_INIT_TEST_DATA: List[
    Tuple[
        Union[Mapping[Text, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
        bool,
        Dict,
        Text,
    ]
] = [
    (
        REQUESTS_MAP,
        True,
        {"key_1": 1},
        "dict of 2 BitrixAPIRequest",
    ),
    (
        REQUESTS_SEQ,
        False,
        {},
        "list of 2 BitrixAPIRequest",
    ),
]


@pytest.mark.parametrize(
    ("requests", "halt", "kwargs", "expected_requests_repr_fragment"),
    _INIT_TEST_DATA,
)
def test_initialization_and_properties_variants(
    requests: Union[Mapping[Text, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
    halt: bool,
    kwargs: Dict,
    expected_requests_repr_fragment: Text,
):
    obj = BitrixAPIBatchesRequest(
        bitrix_token=TOKEN_MOCK,
        bitrix_api_requests=requests,
        halt=halt,
        **kwargs,
    )

    assert obj._bitrix_token is TOKEN_MOCK
    assert obj._halt == halt
    assert obj._kwargs == kwargs
    assert obj._bitrix_api_requests is requests

    if isinstance(requests, Sequence):
        repr_output = repr(obj)
        assert f"halt={halt}" in repr_output
        assert expected_requests_repr_fragment in repr_output

        str_output = str(obj)
        assert obj._API_METHOD in str_output
        assert expected_requests_repr_fragment in str_output


def test_methods_property_with_mapping():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    req1 = BitrixAPIRequest(bitrix_token=token_mock, api_method="user.current")
    req2 = BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.deal.list", params={"filter": {"ID": 123}})

    requests_map = {"me": req1, "deal": req2}
    obj = BitrixAPIBatchesRequest(bitrix_token=token_mock, bitrix_api_requests=requests_map)

    methods = obj._methods

    assert isinstance(methods, dict)
    assert methods["me"] == ("user.current", None)
    assert methods["deal"] == ("crm.deal.list", {"filter": {"ID": 123}})


def test_methods_property_with_sequence():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    req1 = BitrixAPIRequest(bitrix_token=token_mock, api_method="user.current")
    req2 = BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.deal.list", params={"filter": {"ID": 123}})

    requests_seq = [req1, req2]
    obj = BitrixAPIBatchesRequest(bitrix_token=token_mock, bitrix_api_requests=requests_seq)

    methods = obj._methods

    assert isinstance(methods, list)
    assert methods[0] == ("user.current", None)
    assert methods[1] == ("crm.deal.list", {"filter": {"ID": 123}})


def test_call_method_delegates_to_call_batches():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    token_mock.call_batches.return_value = RESPONSE_DICT

    requests_map: Mapping[Text, BitrixAPIRequest] = {
        "c1": BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.contact.get", params={"ID": 1}),
        "c2": BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.contact.get", params={"ID": 2}),
    }

    expected_methods = {
        "c1": ("crm.contact.get", {"ID": 1}),
        "c2": ("crm.contact.get", {"ID": 2}),
    }

    obj = BitrixAPIBatchesRequest(
        bitrix_token=token_mock,
        bitrix_api_requests=requests_map,
        halt=True,
        extra_key="extra_val",
    )

    response_dict = obj._call()

    assert response_dict == RESPONSE_DICT

    token_mock.call_batches.assert_called_once_with(
        methods=expected_methods,
        halt=True,
        extra_key="extra_val",
    )


def test_response_and_result_properties():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    token_mock.call_batches.return_value = RESPONSE_DICT

    obj = BitrixAPIBatchesRequest(
        bitrix_token=token_mock,
        bitrix_api_requests=REQUESTS_MAP,
    )

    response = obj.response
    assert isinstance(response, BitrixAPIBatchResponse)
    assert response.result is obj.result
    assert obj._response is response

    response2 = obj.response
    assert response2 is response


def test_response_and_result_properties_with_list():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    token_mock.call_batches.return_value = _RESPONSE_LIST

    obj = BitrixAPIBatchesRequest(
        bitrix_token=token_mock,
        bitrix_api_requests=REQUESTS_SEQ,
    )

    response = obj.response
    assert isinstance(response, BitrixAPIBatchResponse)
    assert response.result is obj.result
    assert obj._response is response


def test_slots_defined():
    assert_slots(BitrixAPIBatchesRequest)
