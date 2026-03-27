# crm.lead.list

## Description
Returns a filtered and ordered list of leads.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.lead.list(
        select=["ID", "TITLE", "STATUS_ID", "OPPORTUNITY", "CURRENCY_ID", "ASSIGNED_BY_ID", "DATE_CREATE"],
        filter={">OPPORTUNITY": 0, "!STATUS_ID": "CONVERTED", "=OPENED": "Y"},
        order={"DATE_CREATE": "DESC", "ID": "DESC"},
        start=0,
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
    bitrix_response = client.crm.lead.list(
        select=["ID", "TITLE", "STATUS_ID"],
        filter={"!STATUS_ID": "JUNK"},
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
    bitrix_response = client.crm.lead.list(
        select=["ID", "TITLE", "STATUS_ID"],
        filter={"!STATUS_ID": "JUNK"},
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
`result` is a list of lead objects; list responses can include `total` for pagination.

## Notes
`crm.lead.list` is list-capable, so both `.as_list()` and `.as_list_fast()` are supported.
