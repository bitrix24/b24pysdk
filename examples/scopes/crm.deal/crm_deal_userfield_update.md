# crm.deal.userfield.update

## Description
Updates an existing custom field for deals.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.userfield.update(
        bitrix_id=42,
        fields={
            "EDIT_FORM_LABEL": {"en": "Priority Score"},
            "LIST_COLUMN_LABEL": {"en": "Priority Score"},
            "LIST_FILTER_LABEL": {"en": "Priority Score"},
            "MANDATORY": "N",
            "SHOW_FILTER": "E",
        },
        list=[
            {"ID": 1, "VALUE": "Low", "SORT": 100},
            {"ID": 2, "VALUE": "High", "SORT": 200},
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
`result` is a boolean (`true` on success).

## Notes
`crm.deal.userfield.update` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
