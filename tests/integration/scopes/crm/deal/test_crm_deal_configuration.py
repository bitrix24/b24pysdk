from typing import Text

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.utils.types import JSONDict

from .....constants import BITRIX_PORTAL_OWNER_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
    pytest.mark.crm_deal_configuration,
]

_SCOPE_PERSONAL: Text = "P"
_SCOPE_COMMON: Text = "C"
_USER_ID: int = BITRIX_PORTAL_OWNER_ID
_DEAL_CATEGORY_ID: int = 0

_CONFIG_DATA: JSONDict = {
    "name": "main",
    "title": f"{SDK_NAME} Deal Configuration",
    "type": "section",
    "elements": [
        {"name": "TITLE"},
        {"name": "STAGE_ID"},
        {"name": "OPPORTUNITY_WITH_CURRENCY"},
    ],
}


@pytest.mark.dependency(name="test_crm_deal_details_configuration_get")
def test_crm_deal_details_configuration_get(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.get(
        scope=_SCOPE_COMMON,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)


@pytest.mark.dependency(name="test_crm_deal_details_configuration_get_with_extras")
def test_crm_deal_details_configuration_get_with_extras(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.get(
        scope=_SCOPE_COMMON,
        extras={"dealCategoryId": _DEAL_CATEGORY_ID},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)


@pytest.mark.oauth_only
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


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_deal_details_configuration_reset", depends=["test_crm_deal_details_configuration_set"])
def test_crm_deal_details_configuration_reset(bitrix_client: BaseClient):
    """"""
    bitrix_response = bitrix_client.crm.deal.details.configuration.reset(
        scope=_SCOPE_PERSONAL,
        user_id=_USER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)
    assert bitrix_response.result is True


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_crm_deal_details_configuration_force_common_scope_for_all")
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
