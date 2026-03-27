# crm.deal.recurring.add

## Description
Creates recurring deal template settings.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.recurring.add(
        fields={
            "TITLE": "Monthly Retainer Renewal",
            "CATEGORY_ID": 0,
            "STAGE_ID": "NEW",
            "IS_ACTIVE": "Y",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 5000,
        },
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
`result` is an integer with the created recurring template ID.

## Notes
`crm.deal.recurring.add` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
