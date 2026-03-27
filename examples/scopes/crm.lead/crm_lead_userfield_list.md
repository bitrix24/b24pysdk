# crm.lead.userfield.list

## Description
Returns lead user fields by filter and order.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.userfield.list(
        filter={"MANDATORY": "N", "SHOW_IN_LIST": "Y"},
        order={"SORT": "ASC", "ID": "DESC"},
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
    bitrix_response = client.crm.lead.userfield.list(
        filter={"SHOW_IN_LIST": "Y"},
        order={"SORT": "ASC"},
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
    bitrix_response = client.crm.lead.userfield.list(
        filter={"SHOW_IN_LIST": "Y"},
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
`result` is a list of user-field objects; list responses can include `total` for pagination.

## Notes
`crm.lead.userfield.list` is list-capable, so both `.as_list()` and `.as_list_fast()` are supported.
