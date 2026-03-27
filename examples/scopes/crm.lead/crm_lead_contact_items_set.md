# crm.lead.contact.items.set

## Description
Replaces the lead's linked contact list.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.contact.items.set(
        bitrix_id=1201,
        items=[
        {"CONTACT_ID": 3401, "SORT": 10, "IS_PRIMARY": "Y"},
        {"CONTACT_ID": 3402, "SORT": 20, "IS_PRIMARY": "N"},
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
`crm.lead.contact.items.set` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
