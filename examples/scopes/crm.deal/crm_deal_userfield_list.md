# crm.deal.userfield.list

## Description
Returns a filtered list of custom fields for deals.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.userfield.list(
        filter={"MANDATORY": "N", "USER_TYPE_ID": "string"},
        order={"SORT": "ASC", "ID": "ASC"},
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

## as_list Example
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.userfield.list(
        filter={"MANDATORY": "N"},
        order={"ID": "ASC"},
    ).as_list().response
    result = bitrix_response.result
    for item in result:
        print(item)
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

## as_list_fast Example
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.userfield.list(
        filter={"MANDATORY": "N"},
        order={"ID": "DESC"},
    ).as_list_fast(descending=True).response
    result = bitrix_response.result
    for item in result:
        print(item)
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
`result` is a collection of user field objects and may include `total`.

## Notes
`crm.deal.userfield.list` is list-capable, so both `.as_list()` and `.as_list_fast()` examples are included.
