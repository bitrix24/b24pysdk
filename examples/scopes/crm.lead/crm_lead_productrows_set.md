# crm.lead.productrows.set

## Description
Creates or replaces product rows for a lead.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.productrows.set(
        bitrix_id=1201,
        rows=[
        {
        "PRODUCT_ID": 456,
        "PRODUCT_NAME": "Enterprise CRM License",
        "PRICE": 1200.0,
        "QUANTITY": 12,
        "DISCOUNT_TYPE_ID": 1,
        "DISCOUNT_SUM": 150.0,
        "TAX_RATE": 20.0,
        "TAX_INCLUDED": "N",
        "MEASURE_CODE": 796,
        "MEASURE_NAME": "pcs",
        "SORT": 10,
        },
        {
        "PRODUCT_NAME": "Implementation Package",
        "PRICE": 5000.0,
        "QUANTITY": 1,
        "DISCOUNT_TYPE_ID": 2,
        "DISCOUNT_RATE": 10.0,
        "TAX_RATE": 20.0,
        "TAX_INCLUDED": "N",
        "MEASURE_CODE": 796,
        "MEASURE_NAME": "pcs",
        "SORT": 20,
        },
        ],
    ).response
    result = bitrix_response.result
    print(result)
except BitrixAPIError as error:
    print(
        "Bitrix API error",
        f"error: {error.error}",
        f"error_description: {error.error_description}",
        sep="\n",
    )
except BitrixSDKException as error:
    print(f"Bitrix SDK error: {error.message}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

## Response Shape
`result` is a boolean (`True` on success).

## Notes
`crm.lead.productrows.set` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
