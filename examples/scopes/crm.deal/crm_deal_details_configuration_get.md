# crm.deal.details.configuration.get

## Description
Returns deal details card configuration.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.details.configuration.get(
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
`result` is a list of configuration sections or `null` if no configuration exists.

## Notes
`crm.deal.details.configuration.get` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
