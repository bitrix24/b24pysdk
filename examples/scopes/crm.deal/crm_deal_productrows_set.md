# crm.deal.productrows.set

## Description
Creates or updates product rows for a deal.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.productrows.set(
        bitrix_id=123,
        rows=[
            {"PRODUCT_ID": 1001, "PRICE": 1200, "QUANTITY": 2, "CURRENCY_ID": "USD", "TAX_RATE": 20},
            {"PRODUCT_NAME": "Implementation Service", "PRICE": 5000, "QUANTITY": 1, "CURRENCY_ID": "USD", "TAX_RATE": 0},
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
`result` is a boolean (`true` on success).

## Notes
`crm.deal.productrows.set` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
