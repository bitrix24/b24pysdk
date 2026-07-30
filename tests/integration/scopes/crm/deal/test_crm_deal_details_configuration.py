from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse, BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.details_configuration import (
    CRMDetailsConfigurationSection,
    CRMDetailsConfigurationSectionData,
)

from .....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
    pytest.mark.crm_deal_details_configuration,
]

_SCOPE_PERSONAL: Text = "P"
_SCOPE_COMMON: Text = "C"
_USER_ID: int = BITRIX_PORTAL_OWNER_ID
_DEAL_CATEGORY_ID: int = 0

_CONFIG_DATA: CRMDetailsConfigurationSectionData = {
    "name": "main",
    "title": f"{SDK_NAME} Deal Configuration",
    "type": "section",
    "elements": [
        {"name": "TITLE"},
        {"name": "STAGE_ID"},
        {"name": "OPPORTUNITY_WITH_CURRENCY"},
    ],
}


def _assert_details_configuration_values(bitrix_response: BitrixAPIValuesResponse):
    assert isinstance(bitrix_response.values, list)

    for section in bitrix_response.values:
        assert isinstance(section, CRMDetailsConfigurationSection)
        assert isinstance(section.elements, list)


@pytest.mark.dependency(name="test_crm_deal_details_configuration_set")
def test_crm_deal_details_configuration_set(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.set(
        data=[_CONFIG_DATA],
        scope=_SCOPE_PERSONAL,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)
    assert bitrix_response.result is True


@pytest.mark.dependency(name="test_crm_deal_details_configuration_get", depends=["test_crm_deal_details_configuration_set"])
def test_crm_deal_details_configuration_get(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.get(
        scope=_SCOPE_PERSONAL,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    _assert_details_configuration_values(bitrix_response)


@pytest.mark.dependency(name="test_crm_deal_details_configuration_get_with_extras", depends=["test_crm_deal_details_configuration_get"])
def test_crm_deal_details_configuration_get_with_extras(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.get(
        scope=_SCOPE_COMMON,
        extras={"dealCategoryId": _DEAL_CATEGORY_ID},
    ).response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    _assert_details_configuration_values(bitrix_response)


@pytest.mark.dependency(name="test_crm_deal_details_configuration_reset", depends=["test_crm_deal_details_configuration_get"])
def test_crm_deal_details_configuration_reset(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.reset(
        scope=_SCOPE_PERSONAL,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)
    assert bitrix_response.result is True


@pytest.mark.dependency(name="test_crm_deal_details_configuration_force_common_scope_for_all", depends=["test_crm_deal_details_configuration_get"])
def test_crm_deal_details_configuration_force_common_scope_for_all(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.force_common_scope_for_all(
        extras={
            "data": [_CONFIG_DATA],
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)
    assert bitrix_response.result is True
