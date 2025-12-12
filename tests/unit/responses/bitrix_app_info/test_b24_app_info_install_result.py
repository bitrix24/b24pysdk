import pytest

from b24pysdk.bitrix_api.responses import B24AppInfoInstallResult
from b24pysdk.constants import B24AppStatus
from b24pysdk.utils.types import JSONDict, JSONList

from ...helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_app_info,
    pytest.mark.b24_app_info_install_result,
]

_JSON_DATA_FULL_INSTALL: JSONDict = {
    "installed": True,
    "version": "2",
    "status": "P",
    "scope": "crm,user,task",
    "domain": "example.bitrix24.com",
    "uri": "https://example.bitrix24.com",
    "client_endpoint": "https://example.bitrix24.com/rest/",
    "member_id": "123456",
    "member_type": "user",
}

_JSON_DATA_FREE_APP: JSONDict = {
    "installed": True,
    "version": "1",
    "status": "F",
    "scope": "crm",
    "domain": "test.bitrix24.com",
    "uri": "https://test.bitrix24.com",
    "client_endpoint": "https://test.bitrix24.com/rest/",
    "member_id": "789012",
    "member_type": "company",
}

_JSON_DATA_DEMO_APP: JSONDict = {
    "installed": False,
    "version": "3",
    "status": "D",
    "scope": "crm,user,calendar,telephony",
    "domain": "demo.bitrix24.com",
    "uri": "https://demo.bitrix24.com",
    "client_endpoint": "https://demo.bitrix24.com/rest/",
    "member_id": "345678",
    "member_type": "user",
}

_JSON_DATA_TRIAL_APP: JSONDict = {
    "installed": True,
    "version": "5",
    "status": "T",
    "scope": "crm,user,task,disk",
    "domain": "trial.bitrix24.com",
    "uri": "https://trial.bitrix24.com",
    "client_endpoint": "https://trial.bitrix24.com/rest/",
    "member_id": "901234",
    "member_type": "company",
}

_JSON_DATA_LOCAL_APP: JSONDict = {
    "installed": True,
    "version": "1",
    "status": "L",
    "scope": "user",
    "domain": "localhost",
    "uri": "https://localhost",
    "client_endpoint": "https://localhost/rest/",
    "member_id": "local123",
    "member_type": "user",
}

_JSON_DATA_SUBSCRIPTION_APP: JSONDict = {
    "installed": True,
    "version": "4",
    "status": "S",
    "scope": "crm,user,task,calendar,telephony,disk",
    "domain": "sub.bitrix24.com",
    "uri": "https://sub.bitrix24.com",
    "client_endpoint": "https://sub.bitrix24.com/rest/",
    "member_id": "567890",
    "member_type": "user",
}

_TEST_DATA: JSONList = [
    _JSON_DATA_FULL_INSTALL,
    _JSON_DATA_FREE_APP,
    _JSON_DATA_DEMO_APP,
    _JSON_DATA_TRIAL_APP,
    _JSON_DATA_LOCAL_APP,
    _JSON_DATA_SUBSCRIPTION_APP,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = B24AppInfoInstallResult.from_dict(json_data)

    assert obj.installed == json_data["installed"]
    assert obj.version == int(json_data["version"])
    assert obj.status == B24AppStatus(json_data["status"])
    assert obj.scope == json_data["scope"].split(",")
    assert obj.domain == json_data["domain"]
    assert obj.uri == json_data["uri"]
    assert obj.client_endpoint == json_data["client_endpoint"]
    assert obj.member_id == json_data["member_id"]
    assert obj.member_type == json_data["member_type"]


def test_frozen_instance():
    assert_frozen_instance(B24AppInfoInstallResult, _JSON_DATA_FULL_INSTALL, "installed")


def test_equality_disabled():
    assert_equality_disabled(B24AppInfoInstallResult, _JSON_DATA_FULL_INSTALL)


def test_is_dataclass():
    assert_is_dataclass(B24AppInfoInstallResult)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(B24AppInfoInstallResult)
