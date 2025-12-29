import pytest

from b24pysdk import Client
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
    BitrixAPIInvalidRequest,
    BitrixAPIMethodConfirmWaiting,
    BitrixAPIMethodNotAllowed,
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
    BitrixOAuthInvalidRequest,
    BitrixOAuthInvalidScope,
    BitrixOauthWrongClient,
)
from tests.env_config import EnvConfig

pytestmark = [
    pytest.mark.integration,
    pytest.mark.test_error,
]

env_config = EnvConfig()


def _assert_error_response(exc: BitrixAPIError, error_cls: type[BitrixAPIError]):
    """Ensure HTTP status and error code (when available) match expected values."""
    assert exc.status_code == error_cls.STATUS_CODE.value

    expected_error = getattr(error_cls, "ERROR", NotImplemented)
    if exc.error and expected_error is not NotImplemented:
        assert exc.error == expected_error


@pytest.mark.oauth_only
def test_error_bitrix_api_bad_request(bitrix_client: Client):
    """"""

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
    """"""

    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )

    with pytest.raises(BitrixAPIUnauthorized) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIUnauthorized)


def test_error_bitrix_api_forbidden():
    """ needed admin agreement https://apidocs.bitrix24.com/api-reference/scopes/confirmation.html """
    pytest.skip(BitrixAPIForbidden.__name__)


# def test_error_bitrix_api_not_found(bitrix_client: Client):
#     """ always get a BitrixAPIBadRequest: Not found """
#
#     created_deal_id = bitrix_client.crm.deal.add(
#         fields={"TITLE": "Test deal for deleting"}
#     ).result
#
#     is_deleted = bitrix_client.crm.deal.delete(
#         bitrix_id=created_deal_id
#     ).response
#
#     bitrix_request = bitrix_client.crm.deal.get(bitrix_id=created_deal_id) if is_deleted else pytest.fail()
#
#     with pytest.raises(BitrixAPINotFound) as exc_info:
#         _ = bitrix_request.response
#
#     _assert_error_response(exc_info.value, BitrixAPINotFound)


def test_error_bitrix_api_method_not_allowed():
    """ cant make request to wrong method """
    pytest.skip(BitrixAPIMethodNotAllowed.__name__)


def test_error_bitrix_api_internal_server_error():
    """"""
    pytest.skip(BitrixAPIInternalServerError.__name__)


def test_error_bitrix_api_service_unavailable():
    """"""
    pytest.skip(BitrixAPIServiceUnavailable.__name__)


@pytest.mark.webhook_only
def test_error_bitrix_api_access_denied(bitrix_client: Client):
    """"""
    bitrix_request = bitrix_client.app.option.get(option="nonexistent_option")

    with pytest.raises(BitrixAPIAccessDenied) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIAccessDenied)


def test_error_bitrix_api_allowed_only_intranet_user():
    """"""
    pytest.skip(BitrixAPIAllowedOnlyIntranetUser.__name__)


def test_error_bitrix_api_insufficient_scope():
    """"""
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
    """ needed admin deny https://apidocs.bitrix24.com/api-reference/scopes/confirmation.html """
    pytest.skip("Requires admin to explicitly deny method confirmation")


def test_error_bitrix_api_user_access_error():
    """"""
    pytest.skip(BitrixAPIUserAccessError.__name__)


@pytest.mark.webhook_only
def test_error_bitrix_api_wrong_auth_type(bitrix_client: Client):
    """"""

    bitrix_request = bitrix_client.placement.bind(
        placement="REST_APP_URI",
        handler="https://example.com/handler",
    )

    with pytest.raises(BitrixAPIWrongAuthType) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIWrongAuthType)


def test_error_bitrix_api_authorization_error():
    """"""
    pytest.skip(BitrixAPIAuthorizationError.__name__)


def test_error_bitrix_api_error_oauth():
    """"""
    pytest.skip(BitrixAPIErrorOAuth.__name__)


def test_error_bitrix_api_expired_token():
    """"""
    pytest.skip(BitrixAPIExpiredToken.__name__)


@pytest.mark.oauth_only
def test_error_bitrix_api_method_confirm_waiting(bitrix_client: Client):
    """"""
    bitrix_request = BitrixAPIRequest(
        bitrix_token=bitrix_client._bitrix_token,
        api_method="voximplant.user.get",
        params={"USER_ID": 1},
    )
    with pytest.raises(BitrixAPIMethodConfirmWaiting) as exc_info:
        _ = bitrix_request.response

    _assert_error_response(exc_info.value, BitrixAPIMethodConfirmWaiting)


def test_error_bitrix_api_no_auth_found():
    """"""
    pytest.skip(BitrixAPINoAuthFound.__name__)


# def test_error_bitrix_api_error_batch_length_exceeded(bitrix_client: Client):
#     """  ValueError: Maximum batch size is 50! """
#
#     bitrix_api_requests = [
#         BitrixAPIRequest(
#             bitrix_token=bitrix_client._bitrix_token,
#             api_method="app.info",
#         )
#         for _ in range(51)
#     ]
#
#     bitrix_request = bitrix_client.call_batch(
#         bitrix_api_requests=bitrix_api_requests,
#         halt=False,
#     )
#
#     with pytest.raises(BitrixAPIErrorBatchLengthExceeded) as exc_info:
#         _ = bitrix_request.response
#
#     _assert_error_response(exc_info.value, BitrixAPIErrorBatchLengthExceeded)


def test_error_bitrix_api_invalid_arg_value():
    """"""
    pytest.skip(BitrixAPIInvalidArgValue.__name__)


def test_error_bitrix_api_invalid_request():
    """"""
    pytest.skip(BitrixAPIInvalidRequest.__name__)


def test_error_bitrix_api_error_manifest_is_not_available():
    """"""
    pytest.skip(BitrixAPIErrorManifestIsNotAvailable.__name__)


# def test_error_bitrix_api_error_batch_method_not_allowed(bitrix_client: Client):
#     """"""
#
#     nested_batch_request = BitrixAPIRequest(
#         bitrix_token=bitrix_client._bitrix_token,
#         api_method="batch",
#         params={"halt": False, "cmd": {"ping": "app.info"}},
#     )
#
#     bitrix_request = bitrix_client.call_batch(
#         bitrix_api_requests=[nested_batch_request],
#         halt=False,
#     )
#
#     with pytest.raises(BitrixAPIErrorBatchMethodNotAllowed) as exc_info:
#         _ = bitrix_request.response
#
#     _assert_error_response(exc_info.value, BitrixAPIErrorBatchMethodNotAllowed)


def test_error_bitrix_api_error_unexpected_answer():
    """"""
    pytest.skip(BitrixAPIErrorUnexpectedAnswer.__name__)


def test_error_bitrix_api_overload_limit():
    """"""
    pytest.skip(BitrixAPIOverloadLimit.__name__)


def test_error_bitrix_api_query_limit_exceeded():
    """"""
    pytest.skip(BitrixAPIQueryLimitExceeded.__name__)


def test_error_bitrix_oauth_wrong_client():
    """"""
    pytest.skip(BitrixOauthWrongClient.__name__)


def test_error_bitrix_oauth_invalid_client():
    """"""
    pytest.skip(BitrixOAuthInvalidClient.__name__)


def test_error_bitrix_oauth_invalid_grant():
    """"""
    pytest.skip(BitrixOAuthInvalidGrant.__name__)


def test_error_bitrix_oauth_invalid_request():
    """"""
    pytest.skip(BitrixOAuthInvalidRequest.__name__)


def test_error_bitrix_oauth_invalid_scope():
    """"""
    pytest.skip(BitrixOAuthInvalidScope.__name__)


def test_error_bitrix_oauth_insufficient_scope():
    """"""
    pytest.skip(BitrixOAuthInsufficientScope.__name__)
