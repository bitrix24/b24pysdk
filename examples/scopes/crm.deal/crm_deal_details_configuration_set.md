# crm.deal.details.configuration.set

## Description
Writes deal details card configuration for a user or common scope.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.details.configuration.set(
        scope="P",
        user_id=1,
        extras={"dealCategoryId": 0},
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
`crm.deal.details.configuration.set` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
