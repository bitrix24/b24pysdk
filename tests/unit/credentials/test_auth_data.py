import pytest

from b24pysdk.api.responses import B24AppInfoResult
from b24pysdk.constants import B24AppStatus
from b24pysdk.credentials.auth import Auth, EventOAuth, RenewedOAuth, WorkflowOAuth
from b24pysdk.utils.types import JSONDict

from ..examples import INSTALL_DATA
from ..helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.credentials,
    pytest.mark.auth_data,
]

_APP_INFO_DATA: JSONDict = {
    "client_id": "local.abc123",
    "scope": "crm,user",
    "expires": "2024-12-31T23:59:59+00:00",
    "install": INSTALL_DATA,
    "user_id": "42",
}

_BASE_AUTH_PAYLOAD: JSONDict = {
    "member_id": INSTALL_DATA["member_id"],
    "client_endpoint": INSTALL_DATA["client_endpoint"],
    "server_endpoint": "https://oauth.bitrix.info/rest/",
    "domain": INSTALL_DATA["domain"],
}

_OAUTH_PAYLOAD: JSONDict = {
    **_BASE_AUTH_PAYLOAD,
    "access_token": "access-token",
    "refresh_token": "refresh-token",
    "expires": 1700000000,
    "expires_in": 3600,
    "user_id": "42",
    "scope": "crm,user",
    "status": "P",
}


def _make_app_info(**overrides: object) -> B24AppInfoResult:
    payload: JSONDict = {**_APP_INFO_DATA, **overrides}
    return B24AppInfoResult.from_dict(payload)


def test_auth_data_from_dict_and_portal_domain():
    obj = Auth.from_dict(_BASE_AUTH_PAYLOAD)

    assert obj.member_id == _BASE_AUTH_PAYLOAD["member_id"]
    assert obj.client_endpoint == _BASE_AUTH_PAYLOAD["client_endpoint"]
    assert obj.server_endpoint == _BASE_AUTH_PAYLOAD["server_endpoint"]
    assert obj.domain == _BASE_AUTH_PAYLOAD["domain"]
    assert obj.portal_domain == INSTALL_DATA["domain"]


def test_auth_data_validate_against_app_info_success():
    obj = Auth.from_dict(_BASE_AUTH_PAYLOAD)
    app_info = _make_app_info()
    assert obj.validate_against_app_info(app_info) is True


def test_auth_data_validate_against_app_info_mismatch():
    obj = Auth.from_dict({**_BASE_AUTH_PAYLOAD, "member_id": "wrong"})
    app_info = _make_app_info()
    with pytest.raises(Auth.ValidationError):
        obj.validate_against_app_info(app_info)


def test_renewed_oauth_token_from_dict():
    obj = RenewedOAuth.from_dict(_OAUTH_PAYLOAD)

    assert obj.oauth_token.access_token == _OAUTH_PAYLOAD["access_token"]
    assert obj.oauth_token.refresh_token == _OAUTH_PAYLOAD["refresh_token"]
    assert obj.user_id == int(_OAUTH_PAYLOAD["user_id"])
    assert obj.scope == _OAUTH_PAYLOAD["scope"].split(",")
    assert obj.status == B24AppStatus(_OAUTH_PAYLOAD["status"])


def test_renewed_oauth_token_to_dict_contains_oauth_token():
    obj = RenewedOAuth.from_dict(_OAUTH_PAYLOAD)
    data = obj.to_dict()

    assert data["oauth_token"]["access_token"] == _OAUTH_PAYLOAD["access_token"]
    assert data["oauth_token"]["refresh_token"] == _OAUTH_PAYLOAD["refresh_token"]


def test_renewed_oauth_token_validate_against_app_info():
    obj = RenewedOAuth.from_dict(_OAUTH_PAYLOAD)
    app_info = _make_app_info()
    assert obj.validate_against_app_info(app_info) is True

    wrong_app_info = _make_app_info(user_id="777")
    with pytest.raises(RenewedOAuth.ValidationError):
        obj.validate_against_app_info(wrong_app_info)


def test_event_oauth_token_minimal_payload():
    payload = {**_BASE_AUTH_PAYLOAD, "application_token": "app-token"}
    obj = EventOAuth.from_dict(payload)

    assert obj.application_token == "app-token"  # noqa: S105
    assert obj.oauth_token is None
    assert obj.user_id is None
    assert obj.scope is None
    assert obj.status is None


def test_event_oauth_token_full_payload_and_validation():
    payload = {
        **_OAUTH_PAYLOAD,
        "application_token": "app-token",
    }
    obj = EventOAuth.from_dict(payload)
    app_info = _make_app_info()

    assert obj.application_token == "app-token"  # noqa: S105
    assert obj.oauth_token is not None
    assert obj.user_id == int(_OAUTH_PAYLOAD["user_id"])
    assert obj.scope == _OAUTH_PAYLOAD["scope"].split(",")
    assert obj.status == B24AppStatus(_OAUTH_PAYLOAD["status"])
    assert obj.validate_against_app_info(app_info) is True


def test_event_oauth_token_validate_allows_missing_user_id():
    payload = {**_BASE_AUTH_PAYLOAD, "application_token": "app-token"}
    obj = EventOAuth.from_dict(payload)
    app_info = _make_app_info(user_id="777")
    assert obj.validate_against_app_info(app_info) is True


def test_workflow_oauth_token_from_dict_and_validation():
    payload = {**_OAUTH_PAYLOAD, "application_token": "app-token"}
    obj = WorkflowOAuth.from_dict(payload)
    app_info = _make_app_info()

    assert obj.application_token == "app-token"  # noqa: S105
    assert obj.validate_against_app_info(app_info) is True


@pytest.mark.parametrize(
    ("cls", "payload"),
    [
        (Auth, {"member_id": "1"}),
        (RenewedOAuth, _BASE_AUTH_PAYLOAD),
        (EventOAuth, _BASE_AUTH_PAYLOAD),
        (WorkflowOAuth, _OAUTH_PAYLOAD),
    ],
)
def test_from_dict_missing_required_fields_raises_validation_error(cls, payload: JSONDict):
    with pytest.raises(cls.ValidationError):
        cls.from_dict(payload)


def test_frozen_instance():
    assert_frozen_instance(Auth, _BASE_AUTH_PAYLOAD, "member_id")
    assert_frozen_instance(RenewedOAuth, _OAUTH_PAYLOAD, "member_id")
    assert_frozen_instance(EventOAuth, {**_BASE_AUTH_PAYLOAD, "application_token": "app-token"}, "member_id")
    assert_frozen_instance(WorkflowOAuth, {**_OAUTH_PAYLOAD, "application_token": "app-token"}, "member_id")


def test_equality_disabled():
    assert_equality_disabled(Auth, _BASE_AUTH_PAYLOAD)
    assert_equality_disabled(RenewedOAuth, _OAUTH_PAYLOAD)
    assert_equality_disabled(EventOAuth, {**_BASE_AUTH_PAYLOAD, "application_token": "app-token"})
    assert_equality_disabled(WorkflowOAuth, {**_OAUTH_PAYLOAD, "application_token": "app-token"})


def test_is_dataclass():
    assert_is_dataclass(Auth)
    assert_is_dataclass(RenewedOAuth)
    assert_is_dataclass(EventOAuth)
    assert_is_dataclass(WorkflowOAuth)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(Auth)
    assert_slots(RenewedOAuth)
    assert_slots(EventOAuth)
    assert_slots(WorkflowOAuth)
