# crm.lead.contact.items.get

## Description
Returns the contact list linked to a lead.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.contact.items.get(
        bitrix_id=1201,
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
`result` is an array of linked contact items.

## Notes
`crm.lead.contact.items.get` returns a relation list but is not a paginated list method, so `.as_list()` and `.as_list_fast()` are not applicable.
