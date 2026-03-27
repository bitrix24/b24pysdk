# crm.deal.update

## Description
Updates an existing deal.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.update(
        bitrix_id=123,
        fields={
            "TITLE": "Enterprise License Renewal - Negotiation",
            "STAGE_ID": "PREPARATION",
            "OPPORTUNITY": 28000,
            "COMMENTS": "Updated after discovery call",
            "ASSIGNED_BY_ID": 1,
        },
        params={"REGISTER_SONET_EVENT": "Y", "REGISTER_HISTORY_EVENT": "Y"},
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
`crm.deal.update` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
