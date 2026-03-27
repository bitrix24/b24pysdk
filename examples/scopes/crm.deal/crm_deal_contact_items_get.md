# crm.deal.contact.items.get

## Description
Returns all contacts linked to a deal.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.contact.items.get(bitrix_id=123).response
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
`result` is a list of deal-contact binding objects.

## Notes
`crm.deal.contact.items.get` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
