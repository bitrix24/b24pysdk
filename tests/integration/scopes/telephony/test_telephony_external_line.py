from typing import Text

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.telephony,
    pytest.mark.telephony_external_line,
]

_CRM_AUTO_CREATE_TRUE: Text = "Y"
_CRM_AUTO_CREATE_FALSE: Text = "N"
_GET_FIELDS = ("NUMBER", "NAME", "CRM_AUTO_CREATE")
_ADD_FIELDS = ("ID",)
_UPDATE_FIELDS = ("ID",)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_line_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    number = f"+7999{int(Config().get_local_datetime().timestamp() * (10 ** 6)) % 1000000000:09d}"
    name = f"{SDK_NAME} LINE"

    bitrix_response = bitrix_client.telephony.external_line.add(
        number=number,
        name=name,
        crm_auto_create=True,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)
    for field in _ADD_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    line_data = bitrix_response.result
    line_id = line_data.get("ID")
    assert isinstance(line_id, int), "Line creation ID should be int"
    assert line_id > 0, "Line creation should return a positive ID"

    cache.set("telephony_external_line_number", number)
    cache.set("telephony_external_line_name", name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_line_get", depends=["test_telephony_external_line_add"])
def test_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    number = cache.get("telephony_external_line_number", None)
    assert isinstance(number, str), "Line number should be cached"

    name = cache.get("telephony_external_line_name", None)
    assert isinstance(name, str), "Line name should be cached"

    bitrix_response = bitrix_client.telephony.external_line.get().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    lines = bitrix_response.result
    matched_lines = [line for line in lines if isinstance(line, dict) and line.get("NUMBER") == number]
    assert len(matched_lines) == 1, "Expected created external line in external_line.get result"

    line = matched_lines[0]
    for field in _GET_FIELDS:
        assert field in line, f"Field '{field}' should be present"
    assert line.get("NAME") == name, "Line NAME does not match"
    assert line.get("CRM_AUTO_CREATE") in (_CRM_AUTO_CREATE_TRUE, _CRM_AUTO_CREATE_FALSE), "Line CRM_AUTO_CREATE has unexpected value"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_line_update", depends=["test_telephony_external_line_get"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    number = cache.get("telephony_external_line_number", None)
    assert isinstance(number, str), "Line number should be cached"

    updated_name = f"{SDK_NAME} LINE UPDATED"

    bitrix_response = bitrix_client.telephony.external_line.update(
        number=number,
        name=updated_name,
        crm_auto_create=False,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)
    for field in _UPDATE_FIELDS:
        assert field in bitrix_response.result, f"Field '{field}' should be present"

    line_data = bitrix_response.result
    line_id = line_data.get("ID")
    assert isinstance(line_id, str), "Line update ID should be string"
    assert int(line_id) > 0, "Line update should return a positive ID"

    cache.set("telephony_external_line_name", updated_name)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_telephony_external_line_delete", depends=["test_telephony_external_line_update"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    number = cache.get("telephony_external_line_number", None)
    assert isinstance(number, str), "Line number should be cached"

    bitrix_response = bitrix_client.telephony.external_line.delete(number=number).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)
    assert len(bitrix_response.result) == 0, "Line delete should return an empty list"
