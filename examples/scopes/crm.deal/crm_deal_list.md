# crm.deal.list

## Description
Returns a filtered and ordered list of deals.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.list(
        select=["ID", "TITLE", "STAGE_ID", "OPPORTUNITY", "ASSIGNED_BY_ID", "DATE_CREATE"],
        filter={">OPPORTUNITY": 1000, "!STAGE_ID": "WON", "=OPENED": "Y"},
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
    bitrix_response = client.crm.deal.list(
        select=["ID", "TITLE", "STAGE_ID"],
        filter={"!STAGE_ID": "LOSE"},
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
    bitrix_response = client.crm.deal.list(
        select=["ID", "TITLE", "STAGE_ID"],
        filter={"!STAGE_ID": "LOSE"},
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
`result` is a list of deal objects; paging fields can include `total` and `next`.

## Notes
`crm.deal.list` is list-capable, so both `.as_list()` and `.as_list_fast()` examples are included.
