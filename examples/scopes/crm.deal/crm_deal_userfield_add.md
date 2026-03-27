# crm.deal.userfield.add

## Description
Creates a custom field for deals.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.userfield.add(
        fields={
            "FIELD_NAME": "UF_CRM_DEAL_PRIORITY_SCORE",
            "USER_TYPE_ID": "integer",
            "XML_ID": "deal_priority_score",
            "SORT": 100,
            "MULTIPLE": "N",
            "MANDATORY": "N",
            "SHOW_FILTER": "E",
            "EDIT_FORM_LABEL": {"en": "Priority Score"},
            "LIST_COLUMN_LABEL": {"en": "Priority Score"},
            "LIST_FILTER_LABEL": {"en": "Priority Score"},
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
`result` is an integer with the created user field ID.

## Notes
`crm.deal.userfield.add` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
