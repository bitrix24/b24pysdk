from datetime import datetime

import pytest

from b24pysdk._config import Config
from b24pysdk.api.responses import B24AppInfoResult
from b24pysdk.credentials.oauth_event_data import OAuthEventData
from b24pysdk.utils.types import JSONDict

from ..examples import INSTALL_DATA
from ..helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.credentials,
    pytest.mark.oauth_event_data,
]

_APP_INFO_DATA: JSONDict = {
    "client_id": "local.abc123",
    "scope": "crm,user",
    "expires": "2024-12-31T23:59:59+00:00",
    "install": INSTALL_DATA,
    "user_id": "42",
}

_BASE_EVENT_PAYLOAD: JSONDict = {
    "event": "ONCRMCONTACTADD",
    "event_handler_id": "7",
    "ts": "1700000000",
    "auth": {
        "member_id": INSTALL_DATA["member_id"],
        "client_endpoint": INSTALL_DATA["client_endpoint"],
        "server_endpoint": "https://oauth.bitrix.info/rest/",
        "domain": INSTALL_DATA["domain"],
        "application_token": "app-token",
    },
}

_OAUTH_EVENT_PAYLOAD: JSONDict = {
    **_BASE_EVENT_PAYLOAD,
    "auth": {
        **_BASE_EVENT_PAYLOAD["auth"],
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "expires": 1700000000,
        "expires_in": 3600,
        "user_id": "42",
        "scope": "crm,user",
        "status": "P",
    },
}


def _make_app_info(**overrides: object) -> B24AppInfoResult:
    payload: JSONDict = {**_APP_INFO_DATA, **overrides}
    return B24AppInfoResult.from_dict(payload)


def test_from_dict_system_event_sets_is_system():
    obj = OAuthEventData.from_dict(_BASE_EVENT_PAYLOAD)

    assert obj.event == _BASE_EVENT_PAYLOAD["event"]
    assert obj.event_handler_id == int(_BASE_EVENT_PAYLOAD["event_handler_id"])
    assert obj.ts == datetime.fromtimestamp(int(_BASE_EVENT_PAYLOAD["ts"]), tz=Config().tz)
    assert obj.is_system is True
    assert obj.auth.oauth_token is None


def test_from_dict_oauth_event_sets_is_system_false():
    obj = OAuthEventData.from_dict(_OAUTH_EVENT_PAYLOAD)

    assert obj.is_system is False
    assert obj.auth.oauth_token is not None


def test_validate_against_app_info_success_and_failure():
    obj = OAuthEventData.from_dict(_OAUTH_EVENT_PAYLOAD)
    app_info = _make_app_info()
    assert obj.validate_against_app_info(app_info) is True

    wrong_app_info = _make_app_info(user_id="777")
    with pytest.raises(OAuthEventData.ValidationError):
        obj.validate_against_app_info(wrong_app_info)


def test_frozen_instance():
    assert_frozen_instance(OAuthEventData, _OAUTH_EVENT_PAYLOAD, "event")


def test_equality_disabled():
    assert_equality_disabled(OAuthEventData, _OAUTH_EVENT_PAYLOAD)


def test_is_dataclass():
    assert_is_dataclass(OAuthEventData)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(OAuthEventData)
