# crm.lead.contact.fields

## Description
Returns metadata for lead-contact relation fields.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.contact.fields().response
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
`result` is an object describing relation fields such as `CONTACT_ID`, `SORT`, and `IS_PRIMARY`.

## Notes
`crm.lead.contact.fields` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
