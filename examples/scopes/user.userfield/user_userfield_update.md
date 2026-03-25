# user.userfield.update

## Description
Updates an existing custom user field by its identifier.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

bitrix_id = 176
fields = {
    "XML_ID": "UF_USR_SKILLS_PROFILE_V2",
    "SORT": 200,
    "MANDATORY": "N",
    "SHOW_FILTER": "Y",
    "SHOW_IN_LIST": "Y",
    "EDIT_IN_LIST": "Y",
    "IS_SEARCHABLE": "Y",
    "SETTINGS": {
        "DEFAULT_VALUE": "Senior Python integration engineer",
        "ROWS": 4,
    },
    "EDIT_FORM_LABEL": {
        "en": "Skills profile",
    },
    "LIST_COLUMN_LABEL": {
        "en": "Skills profile",
    },
    "LIST_FILTER_LABEL": {
        "en": "Skills profile",
    },
    "ERROR_MESSAGE": {
        "en": "Skills profile is invalid",
    },
    "HELP_MESSAGE": {
        "en": "Update the short integration skills summary.",
    },
    "LABEL": "Skills profile",
}

try:
    bitrix_response = client.user.userfield.update(
        bitrix_id=bitrix_id,
        fields=fields,
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
    print("Bitrix SDK error", error.message, sep="\n")
except Exception as error:
    print("Unexpected error", error, sep="\n")
```

## Response Shape
`result` is a boolean and is `True` when the user field update succeeds.

## Notes
`user.userfield.update` is not list-capable, so `.as_list()` and `.as_list_fast()` do not apply.
