# crm.deal.contact.add

## Description
Adds a contact binding to a deal.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.contact.add(
        bitrix_id=123,
        fields={"CONTACT_ID": 456, "SORT": 10, "IS_PRIMARY": "Y"},
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
`result` is a boolean (`true` if added, `false` when binding already exists).

## Notes
`crm.deal.contact.add` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
