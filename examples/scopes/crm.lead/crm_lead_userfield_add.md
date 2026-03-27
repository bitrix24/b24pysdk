# crm.lead.userfield.add

## Description
Creates a custom lead user field.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.userfield.add(
        fields={
        "FIELD_NAME": "UF_CRM_INTEGRATION_PLAN",
        "USER_TYPE_ID": "string",
        "XML_ID": "UF_CRM_INTEGRATION_PLAN",
        "LABEL": "Integration Plan",
        "LIST_FILTER_LABEL": {"en": "Integration Plan"},
        "LIST_COLUMN_LABEL": {"en": "Integration Plan"},
        "EDIT_FORM_LABEL": {"en": "Integration Plan"},
        "ERROR_MESSAGE": {"en": "Integration Plan is invalid"},
        "HELP_MESSAGE": {"en": "Provide implementation scope and milestones."},
        "MULTIPLE": "N",
        "MANDATORY": "N",
        "SHOW_FILTER": "Y",
        "SHOW_IN_LIST": "Y",
        "EDIT_IN_LIST": "Y",
        "IS_SEARCHABLE": "Y",
        "SORT": 300,
        "SETTINGS": {"DEFAULT_VALUE": "Phase 1 discovery", "ROWS": 4},
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
`result` is an integer user field ID.

## Notes
`crm.lead.userfield.add` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
