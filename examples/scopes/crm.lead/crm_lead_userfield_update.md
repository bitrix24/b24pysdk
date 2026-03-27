# crm.lead.userfield.update

## Description
Updates an existing custom lead field.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.userfield.update(
        bitrix_id=410,
        fields={
        "MANDATORY": "N",
        "SHOW_FILTER": "Y",
        "XML_ID": "UF_CRM_INTEGRATION_PLAN",
        "SETTINGS": {"DEFAULT_VALUE": "Phase 2 rollout", "ROWS": 6},
        "SORT": 450,
        "SHOW_IN_LIST": "Y",
        "EDIT_IN_LIST": "Y",
        "IS_SEARCHABLE": "Y",
        "LIST_FILTER_LABEL": {"en": "Integration Plan Filter"},
        "LIST_COLUMN_LABEL": {"en": "Integration Plan Column"},
        "EDIT_FORM_LABEL": {"en": "Integration Plan Form"},
        "ERROR_MESSAGE": {"en": "Integration Plan update failed"},
        "HELP_MESSAGE": {"en": "Keep delivery plan aligned with contract."},
        },
        list=[
        {"VALUE": "Discovery", "DEF": "N", "XML_ID": "DISCOVERY", "SORT": 100},
        {"VALUE": "Rollout", "DEF": "N", "XML_ID": "ROLLOUT", "SORT": 200},
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
`crm.lead.userfield.update` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
