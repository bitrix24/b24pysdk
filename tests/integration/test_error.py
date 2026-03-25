from __future__ import annotations

# from contextlib import suppress
from typing import Dict, Optional, Text, Type

import pytest
import requests

# noinspection PyProtectedMember
from b24pysdk.api.requesters._utils.parse_response import parse_response
from b24pysdk.api.requests import BitrixAPIRequest
from b24pysdk.client import BaseClient, Client
from b24pysdk.credentials import BitrixApp, BitrixToken, BitrixWebhook
from b24pysdk.error import (
    BitrixAPIAccessDenied,
    BitrixAPIAllowedOnlyIntranetUser,
    BitrixAPIApplicationNotFound,
    BitrixAPIAuthorizationError,
    BitrixAPIBadRequest,
    BitrixAPIError,
    BitrixAPIErrorOAuth,
    BitrixAPIErrorUnexpectedAnswer,
    BitrixAPIExpiredToken,
    BitrixAPIInsufficientScope,
    BitrixAPIInvalidArgValue,
    BitrixAPIInvalidCredentials,
    BitrixAPIInvalidToken,
    BitrixAPIMethodConfirmDenied,
    BitrixAPIMethodConfirmWaiting,
    BitrixAPINoAuthFound,
    BitrixAPIOverloadLimit,
    BitrixAPIPaymentRequired,
    BitrixAPIQueryLimitExceeded,
    # BitrixAPITooManyRequests,
    BitrixAPIUnauthorized,
    BitrixAPIUserAccessError,
    BitrixAPIWrongAuthType,
    BitrixRequestTimeout,
    BitrixResponse302JSONDecodeError,
)
from tests.constants import (
    APP_NOT_FOUND_TOKEN,
    APP_NOT_INSTALLED_TOKEN,
    EXTERNAL_USER_WEBHOOK_TOKEN,
    FIRED_USER_TOKEN,
    OLD_DOMAIN,
    PROFILE_ONLY_WEBHOOK_TOKEN,
    RESTRICTED_USER_OAUTH_TOKEN,
    SUBSCRIPTION_ENDED_TOKEN,
)
from tests.env_config import EnvConfig

pytestmark = [
    pytest.mark.integration,
    pytest.mark.test_error,
]

env_config: EnvConfig = EnvConfig()

_REST_BASE_URL: Text = f"https://{env_config.domain}/rest"

_JSON_HEADERS: Dict[Text, Text] = {"Accept": "application/json"}
_REQUEST_TIMEOUT: int = 10
_TINY_TIMEOUT: float = 0.0001

_TEST_ENTITY_TYPE_ID: int = 1268
_TEST_ITEM_ID: int = 1
_EXPIRED_TOKEN: Optional[Text] = env_config.expired_token or None


def _rest_url(path: Text) -> Text:
    return f"{_REST_BASE_URL}/{path.lstrip('/')}"


def _assert_error_response(exc: BitrixAPIError, error_cls: Type[BitrixAPIError]):
    """Ensure HTTP status and error code (when available) match expected values."""

    assert exc.status_code == error_cls.STATUS_CODE

    expected_error = getattr(error_cls, "ERROR", NotImplemented)

    if exc.error and expected_error is not NotImplemented:
        assert exc.error.upper() == expected_error


def test_error_bitrix_api_bad_request(bitrix_client: BaseClient):
    """Expect BitrixAPIBadRequest on CANCELED when sending to an inaccessible chat."""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="im.message.add",
        params={
            "DIALOG_ID": "chat1111",
            "MESSAGE": "test message",
        },
    )

    with pytest.raises(BitrixAPIBadRequest) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIBadRequest)


@pytest.mark.oauth_only
def test_error_bitrix_api_unauthorized(bitrix_client: BaseClient):
    """Unauthorized: inadequate rights for the method."""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )

    with pytest.raises(BitrixAPIUnauthorized) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIUnauthorized)


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


def test_error_bitrix_request_timeout(bitrix_client: BaseClient):
    """Expect BitrixRequestTimeout with an unrealistically small timeout."""

    timeout_client = Client(bitrix_client._bitrix_token, timeout=_TINY_TIMEOUT, max_retries=1)
    profile_request = timeout_client.app.info()

    with pytest.raises(BitrixRequestTimeout) as exc_info:
        _ = profile_request.response

    assert exc_info.value.timeout == _TINY_TIMEOUT


# def test_error_bitrix_api_too_many_requests(bitrix_client: BaseClient):
#     """Attempt to trigger BitrixAPITooManyRequests by spamming updates on the same deal."""
#     deal_id = bitrix_client.crm.deal.add(
#         fields={
#             "TITLE": "B24PySDK TooManyRequests",
#             "STAGE_ID": "NEW",
#             "CURRENCY_ID": "USD",
#             "OPPORTUNITY": 1,
#         },
#     ).response.result
#
#     max_attempts = 1000
#     try:
#         for idx in range(max_attempts):
#             update_request = bitrix_client.crm.deal.update(
#                 bitrix_id=deal_id,
#                 fields={
#                     "COMMENTS": f"rate-limit-test-{idx}",
#                 },
#             )
#             try:
#                 _ = update_request.response
#             except BitrixAPITooManyRequests as error:
#                 _assert_error_response(error, BitrixAPITooManyRequests)
#                 return
#     finally:
#         with suppress(BitrixAPIError):
#             _ = bitrix_client.crm.deal.delete(bitrix_id=deal_id).response
#
#     pytest.skip(f"{BitrixAPITooManyRequests.__name__} not reproduced after {max_attempts} calls")


@pytest.mark.webhook_only
def test_error_bitrix_api_access_denied(bitrix_client: BaseClient):
    """Expect BitrixAPIAccessDenied via webhook call on a restricted plan (works)."""

    bitrix_request = bitrix_client.app.option.get(option="nonexistent_option")

    with pytest.raises(BitrixAPIAccessDenied) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIAccessDenied)


@pytest.mark.webhook_only
def test_error_bitrix_api_allowed_only_intranet_user():
    """Expect ALLOWED_ONLY_INTRANET_USER when calling intranet-only method from external webhook user."""

    if not EXTERNAL_USER_WEBHOOK_TOKEN:
        pytest.skip("Set EXTERNAL_USER_WEBHOOK_TOKEN to run ALLOWED_ONLY_INTRANET_USER scenario")

    external_user_client = Client(
        BitrixWebhook(
            domain=env_config.domain,
            auth_token=EXTERNAL_USER_WEBHOOK_TOKEN,
        ),
    )
    bitrix_request = external_user_client.timeman.status()

    with pytest.raises(BitrixAPIAllowedOnlyIntranetUser) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIAllowedOnlyIntranetUser)


@pytest.mark.webhook_only
def test_error_bitrix_api_insufficient_scope():
    """Expect BitrixAPIInsufficientScope using a profile-only webhook on app scope."""

    if not PROFILE_ONLY_WEBHOOK_TOKEN or PROFILE_ONLY_WEBHOOK_TOKEN is NotImplemented:
        pytest.skip("PROFILE_ONLY_WEBHOOK_TOKEN is not configured")

    limited_client = Client(
        BitrixWebhook(
            domain=env_config.domain,
            auth_token=PROFILE_ONLY_WEBHOOK_TOKEN,
        ),
    )

    bitrix_request = limited_client.crm.lead.fields()

    with pytest.raises(BitrixAPIInsufficientScope) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIInsufficientScope)


@pytest.mark.webhook_only
def test_error_bitrix_api_invalid_credentials():
    """INVALID_CREDENTIALS: Invalid request credentials (invalid webhook token)."""

    invalid_client = Client(
        BitrixWebhook(
            domain=env_config.domain,
            auth_token=f"{env_config.webhook_token}INVALID",
        ),
    )
    bitrix_request = invalid_client.profile()

    with pytest.raises(BitrixAPIInvalidCredentials) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIInvalidCredentials)


@pytest.mark.oauth_only
def test_error_bitrix_api_invalid_token():
    """invalid_token: Unable to get application by token (OAuth access_token)."""

    if not env_config.are_oauth_credentials_available:
        pytest.skip("Missing OAuth credentials")

    invalid_token_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token="INVALID_OAUTH_TOKEN_123", # noqa: S106
            bitrix_app=BitrixApp(
                client_id=env_config.client_id,
                client_secret=env_config.client_secret,
            ),
        ),
    )

    bitrix_request = invalid_token_client.profile()

    with pytest.raises(BitrixAPIInvalidToken) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIInvalidToken)


def test_error_bitrix_api_method_confirm_denied():
    """Requires manual admin denial of method confirmation."""
    pytest.skip(BitrixAPIMethodConfirmDenied.__name__)


@pytest.mark.oauth_only
def test_error_bitrix_api_user_access_error():
    """Expect USER_ACCESS_ERROR with OAuth token of app/user pair that has restricted app access."""

    if not RESTRICTED_USER_OAUTH_TOKEN:
        pytest.skip("Set RESTRICTED_USER_OAUTH_TOKEN to run USER_ACCESS_ERROR scenario")

    restricted_user_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token=RESTRICTED_USER_OAUTH_TOKEN,
        ),
    )
    bitrix_request = restricted_user_client.crm.lead.fields()

    with pytest.raises(BitrixAPIUserAccessError) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIUserAccessError)


@pytest.mark.webhook_only
def test_error_bitrix_api_wrong_auth_type(bitrix_client: BaseClient):
    """Expect WRONG_AUTH_TYPE when using an auth type not allowed for the method (works)."""

    bitrix_request = bitrix_client.placement.bind(
        placement="REST_APP_URI",
        handler="https://example.com/handler",
    )

    with pytest.raises(BitrixAPIWrongAuthType) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIWrongAuthType)


@pytest.mark.webhook_only
def test_error_bitrix_response_302_json_decode_error():
    """Expect BitrixResponse302JSONDecodeError when calling a stale portal domain."""

    if not OLD_DOMAIN or OLD_DOMAIN is NotImplemented:
        pytest.skip("OLD_DOMAIN is not configured")

    old_domain_client = Client(
        BitrixWebhook(
            domain=OLD_DOMAIN,
            auth_token=env_config.webhook_token,
        ),
    )
    bitrix_request = old_domain_client.profile()

    with pytest.raises(BitrixResponse302JSONDecodeError) as exc_info:
        _ = bitrix_request.response

    assert exc_info.value.status_code == BitrixResponse302JSONDecodeError.STATUS_CODE


def test_error_bitrix_api_authorization_error():
    """authorization_error: Unable to authorize user (user is fired/deactivated)."""

    if not FIRED_USER_TOKEN:
        pytest.skip("Set B24_FIRED_USER_TOKEN to run authorization_error scenario")

    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )
    fired_user_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token=FIRED_USER_TOKEN,
            bitrix_app=bitrix_app,
        ),
    )
    bitrix_request = fired_user_client.profile()

    with pytest.raises(BitrixAPIAuthorizationError) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIAuthorizationError)


def test_error_bitrix_api_error_oauth():
    """ERROR_OAUTH: OAuth server says app not installed when portal token cache is expired/missed."""
    if not APP_NOT_INSTALLED_TOKEN:
        pytest.skip("Set B24_APP_NOT_INSTALLED_TOKEN to run ERROR_OAUTH scenario")


    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )
    error_oauth_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token=APP_NOT_INSTALLED_TOKEN,
            bitrix_app=bitrix_app,
        ),
    )
    bitrix_request = error_oauth_client.profile()

    with pytest.raises(BitrixAPIErrorOAuth) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIErrorOAuth)


@pytest.mark.oauth_only
def test_error_bitrix_api_expired_token():
    """expired_token: The access token provided has expired (OAuth token)."""

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


def test_error_bitrix_api_application_not_found():
    """APPLICATION_NOT_FOUND: Portal cache still has token for a deleted app."""
    if not APP_NOT_FOUND_TOKEN:
        pytest.skip("Set B24_APP_NOT_FOUND_TOKEN to run APPLICATION_NOT_FOUND scenario")


    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )
    app_not_found_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token=APP_NOT_FOUND_TOKEN,
            bitrix_app=bitrix_app,
        ),
    )
    bitrix_request = app_not_found_client.profile()

    with pytest.raises(BitrixAPIApplicationNotFound) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIApplicationNotFound)


def test_error_bitrix_api_payment_required():
    """PAYMENT_REQUIRED: Subscription has been ended (portal subscription expired)."""
    if not SUBSCRIPTION_ENDED_TOKEN:
        pytest.skip("Set B24_SUBSCRIPTION_ENDED_TOKEN to run PAYMENT_REQUIRED scenario")


    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )
    payment_required_client = Client(
        BitrixToken(
            domain=env_config.domain,
            auth_token=SUBSCRIPTION_ENDED_TOKEN,
            bitrix_app=bitrix_app,
        ),
    )
    bitrix_request = payment_required_client.profile()

    with pytest.raises(BitrixAPIPaymentRequired) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIPaymentRequired)


@pytest.mark.oauth_only
def test_error_bitrix_api_method_confirm_waiting(bitrix_client: BaseClient):
    """Expect METHOD_CONFIRM_WAITING when Bitrix awaits admin approval (works)."""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )
    with pytest.raises(BitrixAPIMethodConfirmWaiting) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIMethodConfirmWaiting)


def test_error_bitrix_api_invalid_arg_value(bitrix_client: BaseClient):
    """Expect INVALID_ARG_VALUE for a request with a nonexistent filter field (works)."""

    bitrix_request = bitrix_client.crm.type.list(
        filter={"non_existent_field_12345": "some_value"},
    )

    with pytest.raises(BitrixAPIInvalidArgValue) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIInvalidArgValue)


def test_error_bitrix_api_error_unexpected_answer():
    """Server-side error; not reliably reproducible."""
    pytest.skip(BitrixAPIErrorUnexpectedAnswer.__name__)


def test_error_bitrix_api_overload_limit():
    """Requires manual API throttling/blocking to hit OVERLOAD_LIMIT."""
    pytest.skip(BitrixAPIOverloadLimit.__name__)


def test_error_bitrix_api_query_limit_exceeded():
    """Requires exceeding Bitrix24 request counters to hit QUERY_LIMIT_EXCEEDED."""
    pytest.skip(BitrixAPIQueryLimitExceeded.__name__)
