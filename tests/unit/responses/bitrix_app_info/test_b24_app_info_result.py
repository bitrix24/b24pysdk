from datetime import datetime

import pytest

from b24pysdk.bitrix_api.responses import B24AppInfoResult
from b24pysdk.utils.types import JSONDict, JSONList

from ...examples import INSTALL_DATA
from ...helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_app_info,
    pytest.mark.b24_app_info_result,
]

_INSTALL_DATA_2: JSONDict = {
    "installed": False,
    "version": "1",
    "status": "F",
    "scope": "crm",
    "domain": "test.bitrix24.com",
    "uri": "https://test.bitrix24.com",
    "client_endpoint": "https://test.bitrix24.com/rest/",
    "member_id": "789012",
    "member_type": "company",
}

_JSON_DATA_FULL_INFO: JSONDict = {
    "client_id": "local.abc123def456",
    "scope": "crm,user,task",
    "expires": "2024-12-31T23:59:59+00:00",
    "install": INSTALL_DATA,
    "user_id": "12345",
}

_JSON_DATA_MINIMAL_SCOPE: JSONDict = {
    "client_id": "local.xyz789",
    "scope": "user",
    "expires": "2024-06-15T12:00:00+00:00",
    "install": _INSTALL_DATA_2,
    "user_id": "67890",
}

_JSON_DATA_DIFFERENT_EXPIRES: JSONDict = {
    "client_id": "local.def456",
    "scope": "crm,user,calendar",
    "expires": "2023-03-10T18:30:00+00:00",
    "install": INSTALL_DATA,
    "user_id": "11111",
}

_JSON_DATA_LONG_SCOPE: JSONDict = {
    "client_id": "local.ghi789",
    "scope": "crm,user,task,calendar,telephony,disk,department",
    "expires": "2024-09-01T00:00:00+00:00",
    "install": _INSTALL_DATA_2,
    "user_id": "22222",
}

_TEST_DATA: JSONList = [
    _JSON_DATA_FULL_INFO,
    _JSON_DATA_MINIMAL_SCOPE,
    _JSON_DATA_DIFFERENT_EXPIRES,
    _JSON_DATA_LONG_SCOPE,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = B24AppInfoResult.from_dict(json_data)

    assert obj.client_id == json_data["client_id"]
    assert obj.scope == json_data["scope"].split(",")
    assert obj.expires == datetime.fromisoformat(json_data["expires"])
    assert obj.user_id == int(json_data["user_id"])

    install_obj = obj.install
    install_data = json_data["install"]

    assert install_obj.installed == install_data["installed"]
    assert install_obj.version == int(install_data["version"])
    assert install_obj.scope == install_data["scope"].split(",")
    assert install_obj.domain == install_data["domain"]
    assert install_obj.uri == install_data["uri"]
    assert install_obj.client_endpoint == install_data["client_endpoint"]
    assert install_obj.member_id == install_data["member_id"]
    assert install_obj.member_type == install_data["member_type"]


def test_frozen_instance():
    assert_frozen_instance(B24AppInfoResult, _JSON_DATA_FULL_INFO, "client_id")


def test_equality_disabled():
    assert_equality_disabled(B24AppInfoResult, _JSON_DATA_FULL_INFO)


def test_is_dataclass():
    assert_is_dataclass(B24AppInfoResult)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(B24AppInfoResult)
