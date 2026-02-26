from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_deal,
    pytest.mark.crm_deal_productrows,
]

_ROWS_FIELDS: Tuple[Text, ...] = ("PRODUCT_NAME", "PRICE", "QUANTITY")
_ROW_PRODUCT_NAME: Text = f"{SDK_NAME} Product"
_ROW_PRICE: Text = "100.00"
_ROW_QUANTITY: float = 2


@pytest.mark.dependency(name="test_crm_deal_productrows_set")
def test_crm_deal_productrows_set(bitrix_client: BaseClient, cache: Cache):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    deal_title: Text = f"{SDK_NAME} Deal ProductRows {timestamp}"

    deal_response = bitrix_client.crm.deal.add(
        fields={
            "TITLE": deal_title,
            "STAGE_ID": "NEW",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 1,
        },
    ).response

    assert isinstance(deal_response, BitrixAPIResponse)
    assert isinstance(deal_response.result, int)

    deal_id = deal_response.result
    assert deal_id > 0, "Deal creation should return a positive ID"

    bitrix_response = bitrix_client.crm.deal.productrows.set(
        bitrix_id=deal_id,
        rows=[
            {
                "PRODUCT_NAME": _ROW_PRODUCT_NAME,
                "PRICE": _ROW_PRICE,
                "QUANTITY": _ROW_QUANTITY,
            },
        ],
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)
    assert bitrix_response.result is True, "Product rows set should return True"

    cache.set("deal_productrows_deal_id", deal_id)


@pytest.mark.dependency(name="test_crm_deal_productrows_get", depends=["test_crm_deal_productrows_set"])
def test_crm_deal_productrows_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    deal_id = cache.get("deal_productrows_deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    bitrix_response = bitrix_client.crm.deal.productrows.get(
        bitrix_id=deal_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    rows = bitrix_response.result
    assert len(rows) >= 1, "Expected at least one product row"

    row = rows[0]
    assert isinstance(row, dict)

    for field in _ROWS_FIELDS:
        assert field in row, f"Field '{field}' should be present"

    assert row.get("PRODUCT_NAME") == _ROW_PRODUCT_NAME, "PRODUCT_NAME does not match"
    assert float(row.get("PRICE", 0)) == float(_ROW_PRICE), "PRICE does not match"
    assert float(row.get("QUANTITY", 0)) == float(_ROW_QUANTITY), "QUANTITY does not match"


@pytest.mark.dependency(name="test_crm_deal_productrows_cleanup", depends=["test_crm_deal_productrows_get"])
def test_crm_deal_productrows_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    deal_id = cache.get("deal_productrows_deal_id", None)
    assert isinstance(deal_id, int), "Deal ID should be cached"

    deal_delete = bitrix_client.crm.deal.delete(bitrix_id=deal_id).response
    assert isinstance(deal_delete, BitrixAPIResponse)
    assert isinstance(deal_delete.result, bool)
    assert deal_delete.result is True, "Deal deletion should return True"
