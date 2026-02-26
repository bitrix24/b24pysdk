from datetime import datetime

import pytest

from b24pysdk.api.responses import BitrixAppInfoResponse
from b24pysdk.utils.types import JSONDict, JSONList
from tests.unit.examples import EXAMPLE_TIME_1, EXAMPLE_TIME_2, INSTALL_DATA
from tests.unit.helpers import assert_equality_disabled, assert_frozen_instance, assert_is_dataclass, assert_slots, verify_time

pytestmark = [
    pytest.mark.unit,
    pytest.mark.responses,
    pytest.mark.bitrix_app_info,
    pytest.mark.bitrix_app_info_response,
]


_JSON_DATA_FULL_APP_INFO: JSONDict = {
    "result": {
        "client_id": "local.abc123def456",
        "scope": "crm,user,task",
        "expires": "2024-12-31T23:59:59+00:00",
        "install": INSTALL_DATA,
        "user_id": "12345",
    },
    "time": EXAMPLE_TIME_1,
}

_JSON_DATA_MINIMAL_APP_INFO: JSONDict = {
    "result": {
        "client_id": "local.xyz789",
        "scope": "user",
        "expires": "2024-06-15T12:00:00+00:00",
        "install": INSTALL_DATA,
        "user_id": "67890",
    },
    "time": EXAMPLE_TIME_2,
}

_JSON_DATA_DIFFERENT_EXPIRES: JSONDict = {
    "result": {
        "client_id": "local.def456",
        "scope": "crm,user,calendar",
        "expires": "2023-03-10T18:30:00+00:00",
        "install": INSTALL_DATA,
        "user_id": "11111",
    },
    "time": EXAMPLE_TIME_1,
}

_TEST_DATA: JSONList = [
    _JSON_DATA_FULL_APP_INFO,
    _JSON_DATA_MINIMAL_APP_INFO,
    _JSON_DATA_DIFFERENT_EXPIRES,
]


@pytest.mark.parametrize("json_data", _TEST_DATA)
def test_from_dict_variants(json_data: JSONDict):
    obj = BitrixAppInfoResponse.from_dict(json_data)

    result_obj = obj.result
    expected_result = json_data["result"]

    assert result_obj.client_id == expected_result["client_id"]
    assert result_obj.scope == expected_result["scope"].split(",")
    assert result_obj.expires == datetime.fromisoformat(expected_result["expires"])
    assert result_obj.user_id == int(expected_result["user_id"])

    install_obj = result_obj.install
    install_data = expected_result["install"]

    assert install_obj.installed == install_data["installed"]
    assert install_obj.version == int(install_data["version"])
    assert install_obj.scope == install_data["scope"].split(",")
    assert install_obj.domain == install_data["domain"]
    assert install_obj.uri == install_data["uri"]
    assert install_obj.client_endpoint == install_data["client_endpoint"]
    assert install_obj.member_id == install_data["member_id"]
    assert install_obj.member_type == install_data["member_type"]

    verify_time(obj.time, json_data["time"])


def test_frozen_instance():
    assert_frozen_instance(BitrixAppInfoResponse, _JSON_DATA_FULL_APP_INFO, "result")


def test_equality_disabled():
    assert_equality_disabled(BitrixAppInfoResponse, _JSON_DATA_FULL_APP_INFO)


def test_is_dataclass():
    assert_is_dataclass(BitrixAppInfoResponse)


def test_slots_defined_conditionally_by_python_version():
    assert_slots(BitrixAppInfoResponse)
