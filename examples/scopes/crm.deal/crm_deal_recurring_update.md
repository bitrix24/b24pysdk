# crm.deal.recurring.update

## Description
Updates recurring deal template settings.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.recurring.update(
        bitrix_id=77,
        fields={
            "TITLE": "Monthly Retainer Renewal - Updated",
            "IS_ACTIVE": "Y",
            "OPPORTUNITY": 6500,
            "STAGE_ID": "PREPARATION",
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
`result` is a boolean (`true` on success).

## Notes
`crm.deal.recurring.update` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
