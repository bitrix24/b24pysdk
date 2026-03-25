# user.userfield.add

## Description
Adds a new custom user field for the `USER` entity.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

fields = {
    "FIELD_NAME": "UF_USR_SKILLS_PROFILE",
    "USER_TYPE_ID": "string",
    "XML_ID": "UF_USR_SKILLS_PROFILE",
    "SORT": 150,
    "MULTIPLE": "N",
    "MANDATORY": "N",
    "SHOW_FILTER": "Y",
    "SHOW_IN_LIST": "Y",
    "EDIT_IN_LIST": "Y",
    "IS_SEARCHABLE": "Y",
    "SETTINGS": {
        "DEFAULT_VALUE": "Python integration engineer",
        "ROWS": 3,
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
        "en": "Store a short integration skills summary.",
    },
    "LABEL": "Skills profile",
}

try:
    bitrix_response = client.user.userfield.add(
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
`result` is the integer ID of the created user field.

## Notes
`user.userfield.add` is not list-capable, so `.as_list()` and `.as_list_fast()` do not apply.
