import io
from typing import IO, Any, Dict, List, Text, Tuple
from unittest.mock import Mock, patch

import pytest
import requests

from b24pysdk.bitrix_api.requesters.bitrix_api_requester import BitrixAPIRequester
from b24pysdk.error import BitrixRequestError, BitrixRequestTimeout

from ..helpers import assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requesters,
    pytest.mark.bitrix_api_requester,
]

_FILE_IO_1: IO[bytes] = io.BytesIO(b"file_content_1")
_FILE_TUPLE_1: Tuple[Text, IO[bytes]] = ("test.txt", _FILE_IO_1)

_URL_FOR_SINGLE_TESTS: Text = "https://example.bitrix24.com/rest/test.method/"

_INIT_CASE_1: Dict[Text, Any] = {
    "url": "https://example.bitrix24.com/rest/user.get/",
    "params": {"ID": 1, "select": ["ID", "NAME"]},
    "files": {"file": _FILE_TUPLE_1},
    "timeout": 30.0,
    "max_retries": 3,
    "initial_retry_delay": 0.5,
    "retry_delay_increment": 0.5,
}

_INIT_CASE_2: Dict[Text, Any] = {
    "url": "https://example.bitrix24.com/rest/crm.lead.add/",
    "params": {"TITLE": "New Lead"},
    "files": None,
    "timeout": 10.0,
    "max_retries": 1,
    "initial_retry_delay": None,
    "retry_delay_increment": None,
}

_INIT_CASE_3: Dict[Text, Any] = {
    "url": "https://example.bitrix24.com/rest/no.params/",
    "params": None,
    "files": None,
    "max_retries": None,
    "initial_retry_delay": None,
    "retry_delay_increment": None,
}

_INIT_TEST_DATA: List[Dict[Text, Any]] = [
    _INIT_CASE_1,
    _INIT_CASE_2,
    _INIT_CASE_3,
]


@pytest.mark.parametrize("case", _INIT_TEST_DATA)
def test_initialization_and_properties(case):
    obj = BitrixAPIRequester(
        url=case["url"],
        params=case["params"],
        files=case["files"],
        max_retries=case["max_retries"],
        initial_retry_delay=case["initial_retry_delay"],
        retry_delay_increment=case["retry_delay_increment"],
    )

    assert obj._url == case["url"]
    assert obj._params == case["params"]
    assert obj._files == case["files"]


def test_headers_property():
    obj = BitrixAPIRequester(url=_URL_FOR_SINGLE_TESTS)

    with patch.object(BitrixAPIRequester, "_get_default_headers") as mock_default_headers:
        mock_default_headers.return_value = {
            "User-Agent": "TestAgent/1.0",
            "Custom": "Base",
        }

        expected_headers = {
            "User-Agent": "TestAgent/1.0",
            "Custom": "Base",
            "Content-Type": "application/json",
        }

        assert obj._headers == expected_headers


@patch.object(BitrixAPIRequester, "_request_with_retries")
@patch.object(BitrixAPIRequester, "_parse_response")
def test_call_method_delegation(mock_parse, mock_retries):
    mock_response = Mock(spec=requests.Response)
    mock_retries.return_value = mock_response
    mock_parse.return_value = {"success": True}

    obj = BitrixAPIRequester(url=_URL_FOR_SINGLE_TESTS)

    result = obj.call()

    mock_retries.assert_called_once()
    mock_parse.assert_called_once_with(mock_response)
    assert result == {"success": True}


@patch.object(BitrixAPIRequester, "_request_with_retries")
def test_post_raises_bitrix_request_timeout(mock_retries):
    timeout_val = 15.0
    mock_retries.side_effect = requests.Timeout("Original Timeout Message")

    obj = BitrixAPIRequester(url=_URL_FOR_SINGLE_TESTS, timeout=timeout_val)

    with pytest.raises(BitrixRequestTimeout) as excinfo:
        obj._post()

    assert excinfo.type is BitrixRequestTimeout
    assert excinfo.value.timeout == timeout_val
    assert isinstance(excinfo.value.original_error, requests.Timeout)


@patch.object(BitrixAPIRequester, "_request_with_retries")
def test_post_raises_bitrix_request_error(mock_retries):
    mock_retries.side_effect = requests.RequestException("Original Connection Message")

    obj = BitrixAPIRequester(url=_URL_FOR_SINGLE_TESTS)

    with pytest.raises(BitrixRequestError) as excinfo:
        obj._post()

    assert excinfo.type is BitrixRequestError
    assert isinstance(excinfo.value.original_error, requests.RequestException)


def test_slots_defined():
    assert_slots(BitrixAPIRequester)


@patch.object(BitrixAPIRequester, "_request_with_retries")
def test_call_with_retry_parameters(mock_retries):
    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {"result": "test"}
    mock_response.status_code = 200
    mock_retries.return_value = mock_response

    obj = BitrixAPIRequester(
        url=_URL_FOR_SINGLE_TESTS,
        max_retries=5,
        initial_retry_delay=1.0,
        retry_delay_increment=2.0,
    )

    with patch.object(BitrixAPIRequester, "_parse_response") as mock_parse:
        mock_parse.return_value = {"result": "test"}
        result = obj.call()

        assert result == {"result": "test"}
        mock_retries.assert_called_once()
