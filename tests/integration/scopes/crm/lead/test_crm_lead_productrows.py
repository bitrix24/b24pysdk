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
    pytest.mark.crm_lead,
    pytest.mark.crm_lead_productrows,
]

_ROWS_FIELDS: Tuple[Text, ...] = ("PRODUCT_NAME", "PRICE", "QUANTITY")
_ROW_PRODUCT_NAME: Text = f"{SDK_NAME} Lead Product"
_ROW_PRICE: Text = "100.00"
_ROW_QUANTITY: float = 2


@pytest.mark.dependency(name="test_crm_lead_productrows_set")
def test_crm_lead_productrows_set(bitrix_client: BaseClient, cache: Cache):
    """"""

    timestamp = int(Config().get_local_datetime().timestamp() * (10 ** 6))
    lead_title: Text = f"{SDK_NAME} Lead ProductRows {timestamp}"

    lead_response = bitrix_client.crm.lead.add(
        fields={
            "TITLE": lead_title,
            "STATUS_ID": "NEW",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 1,
        },
    ).response

    assert isinstance(lead_response, BitrixAPIResponse)
    assert isinstance(lead_response.result, int)

    lead_id = lead_response.result
    assert lead_id > 0, "Lead creation should return a positive ID"

    bitrix_response = bitrix_client.crm.lead.productrows.set(
        bitrix_id=lead_id,
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

    cache.set("lead_productrows_lead_id", lead_id)


@pytest.mark.dependency(name="test_crm_lead_productrows_get", depends=["test_crm_lead_productrows_set"])
def test_crm_lead_productrows_get(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_productrows_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    bitrix_response = bitrix_client.crm.lead.productrows.get(
        bitrix_id=lead_id,
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


@pytest.mark.dependency(name="test_crm_lead_productrows_cleanup", depends=["test_crm_lead_productrows_get"])
def test_crm_lead_productrows_cleanup(bitrix_client: BaseClient, cache: Cache):
    """"""

    lead_id = cache.get("lead_productrows_lead_id", None)
    assert isinstance(lead_id, int), "Lead ID should be cached"

    lead_delete = bitrix_client.crm.lead.delete(bitrix_id=lead_id).response
    assert isinstance(lead_delete, BitrixAPIResponse)
    assert isinstance(lead_delete.result, bool)
    assert lead_delete.result is True, "Lead deletion should return True"
