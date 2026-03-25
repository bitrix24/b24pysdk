# user.userfield.list

## Description
Returns user fields filtered and sorted by supported user field attributes.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

order = {
    "ID": "desc",
    "SORT": "asc",
}
filter = {
    "USER_TYPE_ID": "string",
    "SHOW_IN_LIST": "Y",
}

try:
    bitrix_response = client.user.userfield.list(
        order=order,
        filter=filter,
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

## as_list Example
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

order = {
    "ID": "desc",
}
filter = {
    "SHOW_IN_LIST": "Y",
}

try:
    bitrix_response = client.user.userfield.list(
        order=order,
        filter=filter,
    ).as_list().response
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

## as_list_fast Example
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

order = {
    "ID": "desc",
}
filter = {
    "SHOW_IN_LIST": "Y",
}

try:
    bitrix_response = client.user.userfield.list(
        order=order,
        filter=filter,
    ).as_list_fast(descending=True).response
    result = bitrix_response.result
    print(list(result))
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
`result` is a list of user field objects. Each item can include keys such as `ID`, `ENTITY_ID`, `FIELD_NAME`, `USER_TYPE_ID`, flags like `SHOW_IN_LIST`, and nested `SETTINGS`. The REST response also includes `total`.

## Notes
`user.userfield.list` is list-capable, so both `.as_list()` and `.as_list_fast()` are available.
