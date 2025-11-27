# Architectural Analysis of Bitrix24 Python SDK

## Project Overview

The Bitrix24 Python SDK, `B24PySDK`, is an official library designed for seamless integration with the Bitrix24 REST API. It provides a clean, Pythonic interface with features like strong typing, token auto-renewal, and efficient handling of large datasets through batch operations.

## Project Architecture

### Directory Structure

```plaintext
b24pysdk/
├── bitrix_api/                # API communication and credential handling
│   ├── credentials/           # Core classes for requests, responses, events
│   ├── events/                # Core classes for requests, responses, events
│   ├── functions/             # API function utilities and methods
│   ├── protocols/             # API function utilities and methods
│   ├── requesters/            # Handling different request types
│   ├── requests/              # API function utilities and methods
│   ├── responses/             # API function utilities and methods
│   └── signals/               # Handling different request types
├── constants/                 # Constant definitions
│   └── crm.py                 # Constant definitions for CRM scope
├── log/                       # Logging utilities
│   ├── abstract_logger.py     # Logger interface required to implement
│   ├── base_logger.py         # Abstract logger class with basic logger interface implementation
│   ├── null_logger.py         # Null implementation of base logger
│   └── stream_logger.py       # Base logger implementation for console logging
├── scopes/                    # Implemented API scopes (CRM, User, etc.)
│   ├── app/                   # App related scope module
│   ├── crm/                   # CRM related scope modules
│   ├── user/                  # User management scope modules
│   ├── socialnetwork/         # Social network related scope modules
│   ├── access.py              # Access related scope module
│   ├── department.py          # Department related scope module
│   ├── feature.py             # Fearure related scope module
│   ├── method.py              # Method related scope module
│   ├── profile.py             # Profile related scope module
│   ├── scope.py               # Scope related scope module
│   └── server.py              # Server related scope module
├── utils/                     # Utility functions and helpers
├── error.py                   # Error handling and exceptions
├── _client.py                 # Client initialization and setup
├── _config.py                 # Configuration and settings management
├── _constants.py              # Constant values for internal use
└── _version.py                # Versioning information
```

### Abstraction Levels

- **HTTP/JSON Protocol**: Basis for communication with Bitrix24.
- **Python Requests**: Used underneath for REST API interactions.
- **Core Client**: Manages token and API interaction, responsible for setting up different scopes.
### Key Components

1. **Client**:
   - **CRM**: Manages customer relationship entities like deals, contacts.
   - **User**: Handles user information and operations.
   - **Socialnetwork**: Responsible for social network interactions.
   - **Department**: Focuses on operations related to departments.

2. **Batch Processing**
   - **Call Batch**: Facilitates batch requests utilizing BitrixAPIBatchRequest.
   - **Call Batches**: Enables the processing of multiple batch requests using BitrixAPIBatchesRequest.

3. **Bitrix API Classes and Functions**: Underlying structures for handling request-response cycles and maintaining API credentials.

### Implementation Patterns

1. **Main Client**: Abstracts the underlying communication mechanisms to facilitate CRUD operations seamlessly.
2. **Batch Operations**: Efficiently manages batch requests, crucial for handling large datasets.
3. **Configuration**: Adjustable settings included in `_config.py` to manage API call timeouts, retry mechanisms, and token configurations for robust performance.
4. **Error Handling**:
     - Implements comprehensive error management via `BitrixAPIError` and `BitrixRequestTimeout` from `error.py`.
     - Provides detailed error descriptions for problematic API calls, enhancing debugging and reliability.

### Standard API Methods

- `add(fields)` - Add new items.
- `get(id)` - Retrieve specific items.
- `list(order, filter, select, start)` - List items.
- `update(id, fields)` - Update existing items.
- `delete(id)` - Delete items.
- `fields()` - Retrieve field metadata.

# Use Cases

### Fields

There is a method .fields() that provides fields of entities.
Example: Get a lable of the userfield.

```python
try:
    request = client.crm.item.fields(
        entity_type_id=1268,
        use_original_uf_names="N",
    ).result
    print(request["webformId"]["title"])
except BitrixAPIError as error:
    print(f"API Bitrix error {error.error: {error}}")
except Exception as error:
    print(f"Error: {error}")
```

### Add (Create a Record)

You can add any Bitrix24 entity like CRM deals, user records, etc.
Example: Adding a new deal in CRM

```python
try:
    request = client.crm.deal.add(
        fields={
                "TITLE":"New Deal #1",
                "TYPE_ID":"COMPLEX",
                "CATEGORY_ID":0,
                "STAGE_ID":"PREPARATION",
                "CURRENCY_ID":"EUR",
                "OPPORTUNITY":1000000,
                "IS_MANUAL_OPPORTUNITY":"Y",
                "TAX_VALUE":0.10,
                "COMPANY_ID":9,
                "CONTACT_IDS":[84,83],
                "OPENED":"Y",
                "CLOSED":"N",
                "COMMENTS":"Example comment",
                "SOURCE_ID":"CALLBACK",
                "SOURCE_DESCRIPTION":"Additional information about the source",
                "ADDITIONAL_INFO":"Additional information",
                "UTM_SOURCE":"google",
                "UTM_MEDIUM":"CPC",
                "PARENT_ID_1220":22,
            }, 
        params={
                "REGISTER_SONET_EVENT": "Y",
            }
    )
    print("ID: ", request.result)
except BitrixAPIError as error:
    print(f"API Bitrix error {error.error: {error}}")
except Exception as error:
    print(f"Error: {error}")
```

### Get (Retrieve a Record)

With get method you can fetch details for a specific entity by ID or unique key and get its field values.
Example: Retrieve specific company details

```python
try:
    currency = client.crm.currency.get(bitrix_id="USD").result
    print(currency["LANG"]["de"]["FORMAT_STRING"], currency["LANG"]["de"]["DEC_POINT"])
except BitrixAPIError as error:
    print(f"API Bitrix error {error.error: {error}}")
except Exception as error:
    print(f"Error: {error}")
```

### Update

Modify entities of a specific entity by ID.
Example: Update a departments's head of certain departments.

```python
try:
    request = client.department.update(
        bitrix_id=3, 
        name="New department title", 
        parent=5, 
        uf_head=12,
    )
    
    if request.result:
        print("Department updated.")
except BitrixAPIError as error:
    print(f"API Bitrix error: {error}")
except Exception as error:
    print(f"Error: {error}")
```

### Delete

To remove an entity permanently from the records you can use method .delete().
Example: Delete a particular deal

```python
try: 
    request = client.crm.type.delete(bitrix_id=5)
    if request.result:
        print("Deal deleted successfully.")
except BitrixAPIError as error:
    print(f"API Bitrix error: {error}")
except Exception as error:
    print(f"Error: {error}")
```

### Handling lists
#### .list()

Retrieve up to 50 deals with optional filters.
Example: Obtain a list of CRM deals on 

```python
try:
    request = client.crm.lead.list(
        select=["ID","TITLE"], 
        filter={
                "<=OPPORTUNITY":20000,
                "IS_MANUAL_OPPORTUNITY":"Y"
            }, 
        order={
                "TITLE":"ASC",
            },
        next=50,
    )
    
    for lead in request.result:
        print(lead["ID"], " - ", lead["TITLE"])
except BitrixAPIError as error:
    print(f"API Bitrix error: {error}")
except Exception as error:
    print(f"Error: {error}")
```

#### .as_list()

Retrieve all pages of a list request.
Example: Retrieve more than 50 deals.

```python
try:
    request = client.crm.deal.list().as_list(limit=50)
    for deal in request.result:
        print(deal["TITLE"])
except BitrixAPIError as error:
    print(f"API Bitrix error: {error}")
except Exception as error:
    print(f"Error: {error}")
```

#### .as_list_fast()

Optimized retrieval for very large datasets that returns generator for working with the result.
Example: Efficiently retrieve a large dataset of deals.

```python
try:
    request = client.crm.deal.list().as_list_fast(descending=True)
    for deal in request.result:
        print(deal["TITLE"])
except BitrixAPIError as error:
    print(f"API Bitrix error: {error}")
except Exception as error:
    print(f"Error: {error}")
```
### Error handling
#### Exception Handling (BitrixAPIError)

```plaintext
_HTTPResponse (ABC)
├─ _HTTPResponseOK (200)
├─ _HTTPResponseFound (302)
├─ _HTTPResponseBadRequest (400)
├─ _HTTPResponseUnauthorized (401)
├─ _HTTPResponseForbidden (403)
├─ _HTTPResponseNotFound (404)
├─ _HTTPResponseMethodNotAllowed (405)
├─ _HTTPResponseInternalError (500)
└─ _HTTPResponseServiceUnavailable (503)

BitrixSDKException (Exception)
├─ BitrixOAuthException
├─ BitrixRequestError
│   ├─ BitrixOAuthRequestError
│   ├─ BitrixRequestTimeout
│   │   └─ BitrixOAuthRequestTimeout
│   └─ BitrixResponseJSONDecodeError (_HTTPResponse)
│       ├─ BitrixResponse302JSONDecodeError (_HTTPResponseFound)
│       └─ BitrixResponse500JSONDecodeError (_HTTPResponseInternalError)
├─ BitrixAPIError (_HTTPResponse)
│   ├─ BitrixAPIBadRequest (_HTTPResponseBadRequest)
│   │   ├─ BitrixAPIErrorBatchLengthExceeded
│   │   ├─ BitrixAPIInvalidArgValue
│   │   ├─ BitrixAPIInvalidRequest
│   │   │   └─ BitrixOAuthInvalidRequest (BitrixOAuthException)
│   │   ├─ BitrixOAuthInvalidClient (BitrixOAuthException)
│   │   └─ BitrixOAuthInvalidGrant (BitrixOAuthException)
│   ├─ BitrixAPIUnauthorized (_HTTPResponseUnauthorized)
│   │   ├─ BitrixAPIExpiredToken
│   │   ├─ BitrixAPINoAuthFound
│   │   ├─ BitrixAPIErrorOAuth
│   │   └─ BitrixAPIMethodConfirmWaiting
│   ├─ BitrixAPIForbidden (_HTTPResponseForbidden)
│   │   ├─ BitrixAPIAccessDenied
│   │   ├─ BitrixAPIAllowedOnlyIntranetUser
│   │   ├─ BitrixAPIInsufficientScope
│   │   ├─ BitrixOAuthInvalidScope (BitrixOAuthException)
│   │   ├─ BitrixOAuthInsufficientScope (BitrixOAuthException)
│   │   ├─ BitrixAPIInvalidCredentials
│   │   ├─ BitrixAPIUserAccessError
│   │   └─ BitrixAPIMethodConfirmDenied
│   ├─ BitrixAPINotFound (_HTTPResponseNotFound)
│   │   └─ BitrixAPIErrorManifestIsNotAvailable
│   ├─ BitrixAPIMethodNotAllowed (_HTTPResponseMethodNotAllowed)
│   │   └─ BitrixAPIErrorBatchMethodNotAllowed
│   ├─ BitrixAPIInternalServerError (_HTTPResponseInternalError)
│   │   └─ BitrixAPIErrorUnexpectedAnswer
│   ├─ BitrixAPIServiceUnavailable (_HTTPResponseServiceUnavailable)
│   │   ├─ BitrixAPIOverloadLimit
│   │   └─ BitrixAPIQueryLimitExceeded
│   └─ BitrixOauthWrongClient (BitrixOAuthException, _HTTPResponseOK)
└─ BitrixValidationError
```


Handles API errors gracefully, providing error descriptions for failed method calls.

```python
from b24pysdk import Client
from b24pysdk.error import (
    BitrixAPIError,
    BitrixRequestTimeout,
    BitrixAPIBadRequest,
    BitrixAPIUnauthorized,
    BitrixAPIForbidden,
    BitrixAPINotFound,
    BitrixAPIInternalServerError,
    BitrixAPIServiceUnavailable
)

client = Client()

try:
    request = client.crm.deal.get(bitrix_id=9999).result
except BitrixRequestTimeout as e:
    print("Request timed out:", e)
except BitrixAPIUnauthorized as e:
    print("Unauthorized access:", e)
except BitrixAPINotFound as e:
    print("Resource not found:", e)
except BitrixAPIForbidden as e:
    print("Access forbidden:", e)
except BitrixAPIInternalServerError as e:
    print("Internal server error:", e)
except BitrixAPIServiceUnavailable as e:
    print("Service unavailable:", e)
except BitrixAPIBadRequest as e:
    print("Bad requests:", e)
except BitrixAPIError as e:
    print("API Error:", e.error_description)
```

### Batch requests

#### Batch Request for Multiple Companies

Executes multiple API calls in a single request, useful for reducing request overhead.

```python
requests_data = {
    "company1": client.crm.company.add(
        fields={
            "ASSIGNED_BY_ID": 100,
            "TITLE": "Updated Company 1",
            "PHONE": [{"VALUE": "+1234567890", "VALUE_TYPE": "WORK"}],
            # Additional fields can be added here
        }
    ),
    "company2": client.crm.company.add(
        fields={
            "ASSIGNED_BY_ID": 101,
            "TITLE": "Updated Company 2",
            "PHONE": [{"VALUE": "+0987654321", "VALUE_TYPE": "WORK"}],
            # Additional fields can be added here
        }
    ),
    # Add more companies as needed
}

# Execute batch request
batch_request = client.call_batch(methods=requests_data, ignore_size_limit=True)

# Process the results
for key, company in batch_request.result.result.items():
    print(f"{key}: {company['ID']}")
```

#### Multiple Batch Requests

Demonstrates handling large workloads through sequential batch requests.

```python
requests = [
    client.crm.activity.update(bitrix_id=1, fields={"RESPONSIBLE_ID":1}),
    client.crm.activity.update(bitrix_id=2, fields={"RESPONSIBLE_ID":1}),
    # assume more requests
]
batches_request = client.call_batches(methods=requests, halt=True)
for activity in batches_request.result.result:
    print(activity["TITLE"])
```

### Configure Timeouts

Utilizes configuration settings to manage timeouts and retries for API requests.

```python
from b24pysdk import Config
from b24pysdk.log import StreamLogger 

logger = StreamLogger()

cfg = Config()
cfg.configure(
    default_timeout=10,                 # seconds or (connect_timeout, read_timeout)
    default_max_retries=3,              # number of retries on transient errors
    default_initial_retry_delay=1,    # seconds
    default_retry_delay_increment=0,  # seconds
    logger=logger,                     
)
```

## Events subscription

By using `OAuthTokenRenewedEvent` and `PortalDomainChangedEvent` you can subscribe on token refresh event and domain name change event.

```python
from b24pysdk import BitrixToken
from ..events import OAuthTokenRenewedEvent, PortalDomainChangedEvent


class MyBitrixToken(BitrixToken):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oauth_token_renewed_signal.connect(self.oauth_token_renewed_handler)
        self.portal_domain_changed_signal.connect(self.portal_domain_changed_handler)
        
    def oauth_token_renewed_handler(self, event: OAuthTokenRenewedEvent):
        print(self, f"Renewed oauth token: {event.renewed_oauth_token}")
        
    def portal_domain_changed_handler(self, event: PortalDomainChangedEvent):
        print(self, f"Old domain: {event.old_domain}, new domain: {event.new_domain}")
```