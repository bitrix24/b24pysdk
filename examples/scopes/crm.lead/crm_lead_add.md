# crm.lead.add

## Description
Creates a new lead.

## Regular Example (Python SDK)
```python
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError, BitrixSDKException
from datetime import datetime

client: BaseClient

lead_birthdate = datetime(1989, 7, 14).date().isoformat()

try:
    bitrix_response = client.crm.lead.add(
        fields={
        "TITLE": "Acme Industrial Subscription",
        "NAME": "Jordan",
        "SECOND_NAME": "Avery",
        "LAST_NAME": "Miller",
        "STATUS_ID": "NEW",
        "OPENED": "Y",
        "ASSIGNED_BY_ID": 1,
        "CURRENCY_ID": "USD",
        "OPPORTUNITY": 25000.0,
        "IS_MANUAL_OPPORTUNITY": "Y",
        "SOURCE_ID": "WEB",
        "SOURCE_DESCRIPTION": "Inbound product comparison form",
        "COMMENTS": "Requested enterprise onboarding call next week.",
        "COMPANY_TITLE": "Acme Industrial LLC",
        "POST": "Procurement Director",
        "BIRTHDATE": lead_birthdate,
        "PHONE": [{"VALUE": "+12025550119", "VALUE_TYPE": "WORK"}],
        "EMAIL": [{"VALUE": "jordan.miller@acme-industrial.com", "VALUE_TYPE": "WORK"}],
        "WEB": [{"VALUE": "https://acme-industrial.com", "VALUE_TYPE": "WORK"}],
        "UTM_SOURCE": "google-ads",
        "UTM_MEDIUM": "cpc",
        "UTM_CAMPAIGN": "q1_enterprise_leads",
        "UTM_CONTENT": "landing_form_variant_a",
        "UTM_TERM": "industrial crm integration",
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
`result` is an integer lead ID.

## Notes
`crm.lead.add` is not list-capable, so `.as_list()` and `.as_list_fast()` are not applicable.
