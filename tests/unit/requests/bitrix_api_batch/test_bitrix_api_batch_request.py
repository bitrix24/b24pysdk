from typing import Dict, List, Mapping, Sequence, Text, Tuple, Union
from unittest.mock import Mock

import pytest

from b24pysdk.bitrix_api.credentials import AbstractBitrixToken
from b24pysdk.bitrix_api.requests.bitrix_api_batch_request import BitrixAPIBatchRequest
from b24pysdk.bitrix_api.requests.bitrix_api_request import BitrixAPIRequest

from ...examples import REQUESTS_MAP, REQUESTS_SEQ, RESPONSE_DICT, TOKEN_MOCK
from ...helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requests,
    pytest.mark.bitrix_api_batch_request,
]


_INIT_TEST_DATA: List[
    Tuple[
        Union[Mapping[Text, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
        bool,
        bool,
        Dict,
        Text,
    ]
] = [
    (
        REQUESTS_MAP,
        True,
        True,
        {"key_1": 1},
        "dict of 2 BitrixAPIRequest",
    ),
    (
        REQUESTS_SEQ,
        False,
        False,
        {},
        "list of 2 BitrixAPIRequest",
    ),
]


@pytest.mark.parametrize(
    ("requests", "halt", "ignore_size_limit", "kwargs", "expected_requests_repr_fragment"),
    _INIT_TEST_DATA,
)
def test_initialization_and_properties_variants(
    requests: Union[Mapping[Text, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
    halt: bool,
    ignore_size_limit: bool,
    kwargs: Dict,
    expected_requests_repr_fragment: Text,
):
    obj = BitrixAPIBatchRequest(
        bitrix_token=TOKEN_MOCK,
        bitrix_api_requests=requests,
        halt=halt,
        ignore_size_limit=ignore_size_limit,
        **kwargs,
    )

    assert obj._bitrix_token is TOKEN_MOCK
    assert obj._halt == halt
    assert obj._kwargs == kwargs
    assert obj._ignore_size_limit == ignore_size_limit

    if isinstance(requests, Sequence):
        repr_output = repr(obj)
        assert f"halt={halt}" in repr_output
        assert f"ignore_size_limit={ignore_size_limit}" in repr_output
        assert expected_requests_repr_fragment in repr_output


def test_call_method_delegates_to_call_batch():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    token_mock.call_batch.return_value = RESPONSE_DICT

    requests_map: Mapping[Text, BitrixAPIRequest] = {
        "c1": BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.contact.get", params={"ID": 1}),
        "c2": BitrixAPIRequest(bitrix_token=token_mock, api_method="crm.contact.get", params={"ID": 2}),
    }

    expected_methods = {
        "c1": ("crm.contact.get", {"ID": 1}),
        "c2": ("crm.contact.get", {"ID": 2}),
    }

    obj = BitrixAPIBatchRequest(
        bitrix_token=token_mock,
        bitrix_api_requests=requests_map,
        halt=True,
        ignore_size_limit=True,
        extra_key="extra_val",
    )

    response_dict = obj._call()

    assert response_dict == RESPONSE_DICT

    token_mock.call_batch.assert_called_once_with(
        methods=expected_methods,
        halt=True,
        ignore_size_limit=True,
        extra_key="extra_val",
    )


def test_response_and_result_properties():
    token_mock: AbstractBitrixToken = Mock(spec=AbstractBitrixToken)
    token_mock.call_batch.return_value = RESPONSE_DICT

    obj = BitrixAPIBatchRequest(
        bitrix_token=token_mock,
        bitrix_api_requests=REQUESTS_MAP,
    )

    response = obj.response
    from b24pysdk.bitrix_api.responses import BitrixAPIBatchResponse
    assert isinstance(response, BitrixAPIBatchResponse)
    assert response.result is obj.result
    assert obj._response is response

    response2 = obj.response
    assert response2 is response


def test_slots_defined():
    assert_slots(BitrixAPIBatchRequest)
