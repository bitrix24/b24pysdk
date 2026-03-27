# crm.deal.add

## Description
Creates a new deal.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

client: BaseClient

try:
    bitrix_response = client.crm.deal.add(
        fields={
            "TITLE": "Enterprise License Renewal",
            "TYPE_ID": "SALE",
            "CATEGORY_ID": 0,
            "STAGE_ID": "NEW",
            "CURRENCY_ID": "USD",
            "OPPORTUNITY": 25000,
            "IS_MANUAL_OPPORTUNITY": "Y",
            "ASSIGNED_BY_ID": 1,
            "OPENED": "Y",
            "COMMENTS": "Renewal negotiation in progress",
            "SOURCE_ID": "WEB",
            "UTM_SOURCE": "google",
            "UTM_MEDIUM": "cpc",
            "UTM_CAMPAIGN": "q2_pipeline",
        },
        params={"REGISTER_SONET_EVENT": "Y"},
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
`result` is an integer with the created deal ID.

## Notes
`crm.deal.add` is not list-capable in SDK usage, so `.as_list()` and `.as_list_fast()` examples are not applicable.
