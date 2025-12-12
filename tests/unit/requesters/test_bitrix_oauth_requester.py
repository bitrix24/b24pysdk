from typing import Text
from unittest.mock import Mock, patch

import pytest
import requests

from b24pysdk.bitrix_api.protocols import BitrixOAuthProtocol
from b24pysdk.bitrix_api.requesters.bitrix_oauth_requester import BitrixOAuthRequester
from b24pysdk.error import (
    BitrixAPIInsufficientScope,
    BitrixAPIInvalidRequest,
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidRequest,
    BitrixOAuthRequestError,
    BitrixOAuthRequestTimeout,
)

pytestmark = [
    pytest.mark.unit,
    pytest.mark.requesters,
    pytest.mark.bitrix_oauth_requester,
]

_CLIENT_ID: Text = "test_client_id"
_CLIENT_SECRET: Text = "test_client_secret"  # noqa: S105
_AUTH_CODE: Text = "test_auth_code"
_REFRESH_TOKEN: Text = "test_refresh_token"  # noqa: S105
_AUTH_TOKEN: Text = "test_auth_token"  # noqa: S105


def create_mock_bitrix_oauth():
    mock = Mock(spec=BitrixOAuthProtocol)
    mock.client_id = _CLIENT_ID
    mock.client_secret = _CLIENT_SECRET
    return mock


def create_requester():
    mock_oauth = create_mock_bitrix_oauth()
    return BitrixOAuthRequester(bitrix_oauth=mock_oauth)


def test_initialization():
    mock_oauth = create_mock_bitrix_oauth()
    timeout_val = 30.0
    max_retries_val = 3
    initial_retry_delay_val = 1.0
    retry_delay_increment_val = 2.0

    obj = BitrixOAuthRequester(
        bitrix_oauth=mock_oauth,
        timeout=timeout_val,
        max_retries=max_retries_val,
        initial_retry_delay=initial_retry_delay_val,
        retry_delay_increment=retry_delay_increment_val,
    )

    assert obj._bitrix_oauth == mock_oauth


def test_headers_property():
    obj = create_requester()

    with patch.object(BitrixOAuthRequester, "_get_default_headers") as mock_default_headers:
        mock_default_headers.return_value = {
            "User-Agent": "TestAgent/1.0",
            "Custom": "Base",
        }

        expected_headers = {
            "User-Agent": "TestAgent/1.0",
            "Custom": "Base",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        assert obj._headers == expected_headers


@patch.object(BitrixOAuthRequester, "_request_with_retries")
def test_get_raises_timeout(mock_request_with_retries):
    mock_oauth = create_mock_bitrix_oauth()
    timeout_val = 15.0

    obj = BitrixOAuthRequester(bitrix_oauth=mock_oauth, timeout=timeout_val)

    mock_request_with_retries.side_effect = requests.Timeout("Timeout error")

    with pytest.raises(BitrixOAuthRequestTimeout) as excinfo:
        obj._get(url="https://test.url", params={})

    assert excinfo.type is BitrixOAuthRequestTimeout
    assert excinfo.value.timeout == timeout_val
    assert isinstance(excinfo.value.original_error, requests.Timeout)


@patch.object(BitrixOAuthRequester, "_request_with_retries")
def test_get_raises_request_error(mock_request_with_retries):
    obj = create_requester()
    mock_request_with_retries.side_effect = requests.ConnectionError("Connection error")

    with pytest.raises(BitrixOAuthRequestError) as excinfo:
        obj._get(url="https://test.url", params={})

    assert excinfo.type is BitrixOAuthRequestError
    assert isinstance(excinfo.value.original_error, requests.ConnectionError)


def test_parse_response_converts_api_invalid_request():
    obj = create_requester()

    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 400
    mock_response.url = "https://test.url"
    mock_response.text = "Invalid request"
    mock_response.json.return_value = {"error": "invalid_request", "error_description": "Invalid request"}

    with patch("b24pysdk.bitrix_api.requesters.bitrix_oauth_requester.BaseRequester._parse_response") as mock_base_parse:
        mock_base_parse.side_effect = BitrixAPIInvalidRequest(
            response=mock_response,
            json_response={"error": "invalid_request"},
        )

        with pytest.raises(BitrixOAuthInvalidRequest) as excinfo:
            obj._parse_response(mock_response)

        assert excinfo.type is BitrixOAuthInvalidRequest
        assert excinfo.value.response == mock_response


def test_parse_response_converts_api_insufficient_scope():
    obj = create_requester()

    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 403
    mock_response.url = "https://test.url"
    mock_response.text = "Insufficient scope"
    mock_response.json.return_value = {"error": "insufficient_scope", "error_description": "Insufficient scope"}

    with patch("b24pysdk.bitrix_api.requesters.bitrix_oauth_requester.BaseRequester._parse_response") as mock_base_parse:
        mock_base_parse.side_effect = BitrixAPIInsufficientScope(
            response=mock_response,
            json_response={"error": "insufficient_scope"},
        )

        with pytest.raises(BitrixOAuthInsufficientScope) as excinfo:
            obj._parse_response(mock_response)

        assert excinfo.type is BitrixOAuthInsufficientScope
        assert excinfo.value.response == mock_response


@patch.object(BitrixOAuthRequester, "_get")
def test_get_oauth_token_success(mock_get):
    obj = create_requester()

    expected_params = {
        "grant_type": "authorization_code",
        "client_id": _CLIENT_ID,
        "client_secret": _CLIENT_SECRET,
        "code": _AUTH_CODE,
    }

    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {"access_token": "new_token", "refresh_token": "new_refresh"}
    mock_get.return_value = mock_response

    with patch("b24pysdk.bitrix_api.requesters.bitrix_oauth_requester.BitrixOAuthRequester._parse_response") as mock_parse:
        mock_parse.return_value = {"access_token": "new_token", "refresh_token": "new_refresh"}
        result = obj.get_oauth_token(code=_AUTH_CODE)

        mock_get.assert_called_once_with(url=BitrixOAuthRequester._OUATH_URL, params=expected_params)
        mock_parse.assert_called_once_with(mock_response)
        assert result == {"access_token": "new_token", "refresh_token": "new_refresh"}


@patch.object(BitrixOAuthRequester, "_get")
def test_refresh_oauth_token_success(mock_get):
    obj = create_requester()

    expected_params = {
        "grant_type": "refresh_token",
        "client_id": _CLIENT_ID,
        "client_secret": _CLIENT_SECRET,
        "refresh_token": _REFRESH_TOKEN,
    }

    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {"access_token": "refreshed_token"}
    mock_get.return_value = mock_response

    with patch("b24pysdk.bitrix_api.requesters.bitrix_oauth_requester.BitrixOAuthRequester._parse_response") as mock_parse:
        mock_parse.return_value = {"access_token": "refreshed_token"}
        result = obj.refresh_oauth_token(refresh_token=_REFRESH_TOKEN)

        mock_get.assert_called_once_with(url=BitrixOAuthRequester._OUATH_URL, params=expected_params)
        mock_parse.assert_called_once_with(mock_response)
        assert result == {"access_token": "refreshed_token"}


@patch.object(BitrixOAuthRequester, "_get")
def test_get_app_info_success(mock_get):
    obj = create_requester()

    expected_params = {
        "auth": _AUTH_TOKEN,
    }

    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {"result": {"APP_ID": "test_app"}, "time": {"start": 1.0, "finish": 2.0}}
    mock_get.return_value = mock_response

    with patch("b24pysdk.bitrix_api.requesters.bitrix_oauth_requester.BitrixOAuthRequester._parse_response") as mock_parse:
        mock_parse.return_value = {"result": {"APP_ID": "test_app"}, "time": {"start": 1.0, "finish": 2.0}}
        result = obj.get_app_info(auth_token=_AUTH_TOKEN)

        mock_get.assert_called_once_with(url=BitrixOAuthRequester._REST_URL, params=expected_params)
        mock_parse.assert_called_once_with(mock_response)
        assert result == {"result": {"APP_ID": "test_app"}, "time": {"start": 1.0, "finish": 2.0}}
