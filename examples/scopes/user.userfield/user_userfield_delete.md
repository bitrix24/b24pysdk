# user.userfield.delete

## Description
Deletes an existing custom user field by its identifier.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

bitrix_id = 176

try:
    bitrix_response = client.user.userfield.delete(
        bitrix_id=bitrix_id,
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
`result` is a boolean and is `True` when the user field is deleted successfully.

## Notes
`user.userfield.delete` is not list-capable, so `.as_list()` and `.as_list_fast()` do not apply.
