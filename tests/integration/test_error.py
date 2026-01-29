from __future__ import annotations

from typing import Dict, Optional, Text, Type

import pytest
import requests

from b24pysdk import Client
from b24pysdk.bitrix_api.requesters._utils.parse_response import parse_response
from b24pysdk.bitrix_api.requests import BitrixAPIRequest
from b24pysdk.error import (
    BitrixAPIAccessDenied,
    BitrixAPIAllowedOnlyIntranetUser,
    BitrixAPIAuthorizationError,
    BitrixAPIBadRequest,
    BitrixAPIError,
    # BitrixAPIErrorBatchLengthExceeded,
    # BitrixAPIErrorBatchMethodNotAllowed,
    BitrixAPIErrorManifestIsNotAvailable,
    BitrixAPIErrorOAuth,
    BitrixAPIErrorUnexpectedAnswer,
    BitrixAPIExpiredToken,
    BitrixAPIForbidden,
    BitrixAPIInsufficientScope,
    BitrixAPIInternalServerError,
    BitrixAPIInvalidArgValue,
    # BitrixAPINotFound,
    BitrixAPIMethodConfirmDenied,
    # BitrixAPIInvalidRequest,
    BitrixAPIMethodConfirmWaiting,
    # BitrixAPIMethodNotAllowed,
    BitrixAPINoAuthFound,
    BitrixAPIOverloadLimit,
    BitrixAPIQueryLimitExceeded,
    BitrixAPIServiceUnavailable,
    BitrixAPIUnauthorized,
    BitrixAPIUserAccessError,
    BitrixAPIWrongAuthType,
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidClient,
    BitrixOAuthInvalidGrant,
    # BitrixOAuthInvalidRequest,
    # BitrixOAuthInvalidScope,
    BitrixOauthWrongClient,
)
from tests.env_config import EnvConfig

pytestmark = [
    pytest.mark.integration,
    pytest.mark.test_error,
]

env_config: EnvConfig = EnvConfig()

_REST_BASE_URL: Text = f"https://{env_config.domain}/rest"
_OAUTH_TOKEN_URL: Text = f"https://{env_config.domain}/oauth/token/"

_JSON_HEADERS: Dict[Text, Text] = {"Accept": "application/json"}
_REQUEST_TIMEOUT: int = 10

_TEST_ENTITY_TYPE_ID: int = 1268
_TEST_ITEM_ID: int = 1
_EXPIRED_TOKEN: Optional[Text] = env_config.expired_token or None


def _rest_url(path: Text) -> Text:
    return f"{_REST_BASE_URL}/{path.lstrip('/')}"


def _assert_error_response(exc: BitrixAPIError, error_cls: Type[BitrixAPIError]):
    """Ensure HTTP status and error code (when available) match expected values."""
    assert exc.status_code == error_cls.STATUS_CODE.value

    expected_error = getattr(error_cls, "ERROR", NotImplemented)
    if exc.error and expected_error is not NotImplemented:
        assert exc.error.upper() == expected_error


@pytest.mark.oauth_only
def test_error_bitrix_api_bad_request(bitrix_client: Client):
    """Expect BitrixAPIBadRequest for an invalid orderentity payload (works)."""

    bitrix_request = bitrix_client.crm.orderentity.add(
        fields={
            "orderId": 1,
            "ownerId": 2,
            "ownerTypeId": 1,
        },
    )

    with pytest.raises(BitrixAPIBadRequest) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIBadRequest)


@pytest.mark.oauth_only
def test_error_bitrix_api_unauthorized(bitrix_client: Client):
    """Expect BitrixAPIUnauthorized on an OAuth call with insufficient rights (works)."""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )

    with pytest.raises(BitrixAPIUnauthorized) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIUnauthorized)


def test_error_bitrix_api_forbidden():
    """Needs portal admin to deny method confirmation per https://apidocs.bitrix24.com/api-reference/scopes/confirmation.html."""
    pytest.skip(BitrixAPIForbidden.__name__)


# def test_error_bitrix_api_not_found(bitrix_client: Client):
#     """Expected NOT_FOUND but Bitrix returns 400 with NOT_FOUND payload (cannot meet 404)."""
#
#     deleting_result = bitrix_client.crm.deal.delete(
#         bitrix_id=11111,
#     )
#
#     with pytest.raises(BitrixAPINotFound) as exc_info:
#         _ = deleting_result.response
#     _assert_error_response(exc_info.value, BitrixAPINotFound)


# def test_error_bitrix_api_method_not_allowed():
#     """GET on POST-only method returns BitrixAPINoAuthFound instead of MethodNotAllowed."""
#
#     deleting_result = requests.get(
#         _rest_url("crm.item.delete"),
#         json={"entityTypeId": _TEST_ENTITY_TYPE_ID, "id": _TEST_ITEM_ID, "auth": _FAKE_AUTH_TOKEN},
#         headers=_JSON_HEADERS,
#     )
#
#     with pytest.raises(BitrixAPIMethodNotAllowed) as exc_info:
#         parse_response(deleting_result)
#     _assert_error_response(exc_info.value, BitrixAPIMethodNotAllowed)


def test_error_bitrix_api_no_auth_found():
    """Expect BitrixAPINoAuthFound when auth is missing in the request (works)."""

    deleting_result = requests.post(
        _rest_url("crm.item.delete"),
        json={"entityTypeId": _TEST_ENTITY_TYPE_ID, "id": _TEST_ITEM_ID},
        headers=_JSON_HEADERS,
        timeout=_REQUEST_TIMEOUT,
    )

    with pytest.raises(BitrixAPINoAuthFound) as exc_info:
        parse_response(deleting_result)
    _assert_error_response(exc_info.value, BitrixAPINoAuthFound)


def test_error_bitrix_api_internal_server_error():
    """No stable way to trigger BitrixAPIInternalServerError; kept skipped."""
    pytest.skip(BitrixAPIInternalServerError.__name__)


def test_error_bitrix_api_service_unavailable():
    """No stable way to trigger BitrixAPIServiceUnavailable; kept skipped."""
    pytest.skip(BitrixAPIServiceUnavailable.__name__)


@pytest.mark.webhook_only
def test_error_bitrix_api_access_denied(bitrix_client: Client):
    """Expect BitrixAPIAccessDenied via webhook call on a restricted plan (works)."""
    bitrix_request = bitrix_client.app.option.get(option="nonexistent_option")

    with pytest.raises(BitrixAPIAccessDenied) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIAccessDenied)


def test_error_bitrix_api_allowed_only_intranet_user():
    """Would require a webhook from an external user to hit ALLOWED_ONLY_INTRANET_USER."""
    pytest.skip(BitrixAPIAllowedOnlyIntranetUser.__name__)


def test_error_bitrix_api_insufficient_scope():
    """Needs a webhook with insufficient permissions to reproduce BitrixAPIInsufficientScope."""
    pytest.skip(BitrixAPIInsufficientScope.__name__)


# @pytest.mark.webhook_only
# def test_error_bitrix_api_invalid_credentials():
#     """ AssertionError: assert 401 == 403 """
#
#     invalid_client = Client(
#         BitrixWebhook(
#             domain=env_config.domain,
#             auth_token=f"{env_config.webhook_token}INVALID",
#         ),
#     )
#     bitrix_request = invalid_client.profile()
#
#     with pytest.raises(BitrixAPIInvalidCredentials) as exc_info:
#         _ = bitrix_request.response
#
#     _assert_error_response(exc_info.value, BitrixAPIInvalidCredentials)


def test_error_bitrix_api_method_confirm_denied():
    """Needs admin to explicitly deny confirmation, similar to the Forbidden scenario."""
    pytest.skip(BitrixAPIMethodConfirmDenied.__name__)


def test_error_bitrix_api_user_access_error():
    """Would need a user token and an app with restricted access to reproduce USER_ACCESS_ERROR."""
    pytest.skip(BitrixAPIUserAccessError.__name__)


@pytest.mark.webhook_only
def test_error_bitrix_api_wrong_auth_type(bitrix_client: Client):
    """Expect WRONG_AUTH_TYPE when using an auth type not allowed for the method (works)."""

    bitrix_request = bitrix_client.placement.bind(
        placement="REST_APP_URI",
        handler="https://example.com/handler",
    )

    with pytest.raises(BitrixAPIWrongAuthType) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIWrongAuthType)


def test_error_bitrix_api_authorization_error():
    """Occurs in isolated-box auth provider flows; not easily reproducible here."""
    pytest.skip(BitrixAPIAuthorizationError.__name__)


def test_error_bitrix_api_error_oauth():
    """Same isolated auth-provider scenario as AuthorizationError; not reproducible here."""
    pytest.skip(BitrixAPIErrorOAuth.__name__)


@pytest.mark.oauth_only
def test_error_bitrix_api_expired_token():
    """Expect BitrixAPIExpiredToken when using an expired OAuth token (works)."""

    if not _EXPIRED_TOKEN:
        pytest.skip("Set B24_EXPIRED_TOKEN to run expired token scenario")

    response = requests.post(
        _rest_url("profile"),
        json={"auth": _EXPIRED_TOKEN},
        headers=_JSON_HEADERS,
        timeout=_REQUEST_TIMEOUT,
    )

    with pytest.raises(BitrixAPIExpiredToken) as exc_info:
        parse_response(response)
    _assert_error_response(exc_info.value, BitrixAPIExpiredToken)


@pytest.mark.oauth_only
def test_error_bitrix_api_method_confirm_waiting(bitrix_client: Client):
    """Expect METHOD_CONFIRM_WAITING when Bitrix awaits admin approval (works)."""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )
    with pytest.raises(BitrixAPIMethodConfirmWaiting) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIMethodConfirmWaiting)


# def test_error_bitrix_api_error_batch_length_exceeded():
#     """SDK limits batch to 50; direct REST with >50 currently does not raise this error."""
#
#
#     batch_url = f"https://{env_config.domain}/rest/{env_config.webhook_token}/batch.json"
#     commands = {f"c{idx}": "app.info" for idx in range(150)}
#
#     response = requests.post(
#         batch_url,
#         json={
#             "halt": False,
#             "cmd": commands,
#         },
#         headers=_JSON_HEADERS,
#     )
#
#     with pytest.raises(BitrixAPIErrorBatchLengthExceeded) as exc_info:
#         parse_response(response)
#
#     _assert_error_response(exc_info.value, BitrixAPIErrorBatchLengthExceeded)


def test_error_bitrix_api_invalid_arg_value():
    """Expect INVALID_ARG_VALUE for a request with a nonexistent filter field (works)."""

    response = requests.post(
        _rest_url(f"{env_config.webhook_token}/crm.type.list"),
        json={
            "filter": {"non_existent_field_12345": "some_value"},
        },
        headers=_JSON_HEADERS,
        timeout=_REQUEST_TIMEOUT,
    )

    with pytest.raises(BitrixAPIInvalidArgValue) as exc_info:
        parse_response(response)

    _assert_error_response(exc_info.value, BitrixAPIInvalidArgValue)


# def test_error_bitrix_api_invalid_request():
#    """"""
#
#    response = requests.post(
#        f"http://{env_config.domain}/rest/placement.get",
#        json={
#            "auth": env_config.access_token,
#        },
#        headers=_JSON_HEADERS,
#    )
#
#    with pytest.raises(BitrixAPIInvalidRequest) as exc_info:
#        parse_response(response)
#
#    _assert_error_response(exc_info.value, BitrixAPIInvalidRequest)


def test_error_bitrix_api_error_manifest_is_not_available():
    """No known stable way to reproduce ERROR_MANIFEST_IS_NOT_AVAILABLE; kept skipped."""
    pytest.skip(BitrixAPIErrorManifestIsNotAvailable.__name__)


# def test_error_bitrix_api_error_batch_method_not_allowed(bitrix_client: Client):
#    """Doc says batching this method should fail, but call didn't return ERROR_BATCH_METHOD_NOT_ALLOWED."""
#
#    batch_url = f"https://{env_config.domain}/rest/{env_config.webhook_token}/batch"
#
#    response = requests.post(
#        batch_url,
#        json={
#            "cmd": {
#                "get_fields1": "tasks.api.scrum.kanban.getFields",
#                "get_fields2": "tasks.api.scrum.kanban.getFields",
#                "get_fields3": "tasks.api.scrum.kanban.getFields",
#                "get_fields4": "tasks.api.scrum.kanban.getFields",
#                "get_fields5": "tasks.api.scrum.kanban.getFields",
#            }
#        },
#        headers=_JSON_HEADERS,
#    )
#
#    with pytest.raises(BitrixAPIErrorBatchMethodNotAllowed) as exc_info:
#        parse_response(response)
#
#    _assert_error_response(exc_info.value, BitrixAPIErrorBatchMethodNotAllowed)


def test_error_bitrix_api_error_unexpected_answer():
    """Server-side unexpected responses are not reproducible reliably; kept skipped."""
    pytest.skip(BitrixAPIErrorUnexpectedAnswer.__name__)


def test_error_bitrix_api_overload_limit():
    """Would require manual API server throttling/blocking to hit OVERLOAD_LIMIT."""
    pytest.skip(BitrixAPIOverloadLimit.__name__)


def test_error_bitrix_api_query_limit_exceeded():
    """Requires exceeding Bitrix24 request counters to hit QUERY_LIMIT_EXCEEDED."""
    pytest.skip(BitrixAPIQueryLimitExceeded.__name__)


def test_error_bitrix_oauth_wrong_client():
    """No reliable info on reproducing WRONG_CLIENT; left skipped."""
    pytest.skip(BitrixOauthWrongClient.__name__)


def test_error_bitrix_oauth_invalid_client():
    """Expect INVALID_CLIENT when using wrong OAuth client credentials (works)."""

    response = requests.post(
        _OAUTH_TOKEN_URL,
        data={
            "client_id": env_config.client_id,
            "client_secret": "WRONG_SECRET_12345",
            "grant_type": "authorization_code",
            "code": "any_valid_or_invalid_code",
        },
        timeout=_REQUEST_TIMEOUT,
    )
    with pytest.raises(BitrixOAuthInvalidClient) as exc_info:
        parse_response(response)
    _assert_error_response(exc_info.value, BitrixOAuthInvalidClient)


def test_error_bitrix_oauth_invalid_grant():
    """Expect INVALID_GRANT when reusing/invalidating an auth code or refresh token (works)."""

    response = requests.post(
        _OAUTH_TOKEN_URL,
        data={
            "client_id": env_config.client_id,
            "client_secret": env_config.client_secret,
            "grant_type": "authorization_code",
            "code": env_config.access_token,
        },
        timeout=_REQUEST_TIMEOUT,
    )

    with pytest.raises(BitrixOAuthInvalidGrant) as exc_info:
        parse_response(response)
    _assert_error_response(exc_info.value, BitrixOAuthInvalidGrant)


# def test_error_bitrix_oauth_invalid_request():
#     """Bitrix returns BitrixAPIInvalidRequest for missing/invalid grant_type instead of OAuthInvalidRequest."""
#     response = requests.post(
#         _OAUTH_TOKEN_URL,
#         data={
#             "client_id": env_config.client_id,
#             "client_secret": env_config.client_secret,
#             "code": "some_code",
#         },
#     )
#     with pytest.raises(BitrixOAuthInvalidRequest) as exc_info:
#         parse_response(response)
#     _assert_error_response(exc_info.value, BitrixOAuthInvalidRequest)


# def test_error_bitrix_oauth_invalid_scope():
#     """Attempt to request disallowed scope should raise INVALID_SCOPE, but not reproduced here."""
#
#     response = requests.post(
#         _OAUTH_TOKEN_URL,
#         data={
#             "client_id": env_config.client_id,
#             "client_secret": env_config.client_secret,
#             "grant_type": "authorization_code",
#         },
#     )
#     with pytest.raises(BitrixOAuthInvalidScope) as exc_info:
#         parse_response(response)
#     _assert_error_response(exc_info.value, BitrixOAuthInvalidScope)


def test_error_bitrix_oauth_insufficient_scope():
    """Could not reproduce OAuth insufficient_scope; left skipped."""
    pytest.skip(BitrixOAuthInsufficientScope.__name__)
