# crm.lead.update

## Description
Updates an existing lead.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException
from datetime import datetime

client: BaseClient

updated_birthdate = datetime(1989, 7, 14).date().isoformat()

try:
    bitrix_response = client.crm.lead.update(
        bitrix_id=1201,
        fields={
        "TITLE": "Acme Industrial Subscription - Negotiation",
        "STATUS_ID": "IN_PROCESS",
        "OPPORTUNITY": 27500.0,
        "CURRENCY_ID": "USD",
        "ASSIGNED_BY_ID": 1,
        "COMMENTS": "Budget approved, waiting for legal review.",
        "SOURCE_DESCRIPTION": "Updated after discovery workshop",
        "BIRTHDATE": updated_birthdate,
        "PHONE": [{"VALUE": "+12025550120", "VALUE_TYPE": "WORK"}],
        "EMAIL": [{"VALUE": "procurement@acme-industrial.com", "VALUE_TYPE": "WORK"}],
        "WEB": [{"VALUE": "https://acme-industrial.com/contact", "VALUE_TYPE": "WORK"}],
        "UTM_SOURCE": "linkedin",
        "UTM_MEDIUM": "paid-social",
        "UTM_CAMPAIGN": "enterprise_followup",
        "UTM_CONTENT": "case_study_ad",
        "UTM_TERM": "crm rollout",
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
`result` is a boolean (`True` on success).

## Notes
`crm.lead.update` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
