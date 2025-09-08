# Bitrix24 REST API Python SDK

================

B24PySDK is the official Python SDK for the Bitrix24 REST API.

Build integrations faster with a clean, Pythonic interface to Bitrix24: strong typing, convenient helpers, and battle‑tested request logic so you can focus on your business logic.

## Key features

- Authentication via OAuth tokens or incoming webhooks
- Native Python types for arguments and responses
- Helpful type hints for available method parameters and their types
- Runtime validation of argument types
- Efficient pagination helpers and batch operations

## Documentation

The REST API documentation can be found on [Bitrix24 REST API](https://apidocs.bitrix24.com/).

## Installation

Requirements: Python 3.9+

Install from PyPI:

```bash
pip install b24pysdk
```

## Library structure at a glance

- Client — entry point for all Bitrix24 calls: `client.crm`, `client.user`, `client.department`, `client.socialnetwork`.
- Authentication:
  - BitrixWebhook — incoming webhook auth
  - BitrixToken — OAuth 2.0 token auth (paired with BitrixApp)
  - BitrixApp — your Bitrix24 app credentials (client_id, client_secret)
- Responses expose `result` and `time` (including execution duration)

## Quickstart

This section provides a short guide to help you get started with B24PySDK.

### Calling an API method

To call the Bitrix24 API, import `Client` and use either `BitrixWebhook` or `BitrixToken` for authentication.
There are two ways to authenticate:

1. Using a permanent incoming local webhook code: <https://apidocs.bitrix24.com/local-integrations/local-webhooks.html>

```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(domain="your_bitrix_portal", auth_token="key_of_your_webhook")
client = Client(bitrix_token)
```

1. Using a temporary OAuth 2.0 authorization token: <https://apidocs.bitrix24.com/api-reference/oauth/index.html>

```python
from b24pysdk import BitrixToken, Client, BitrixApp

bitrix_app = BitrixApp(client_id="app_code", client_secret="app_key")
bitrix_token = BitrixToken(
    domain="your_bitrix_portal",
    auth_token="key_of_your_webhook",
    refresh_token="refresh_token_of_the_app",  # optional parameter
    bitrix_app=bitrix_app,
)
client = Client(bitrix_token)
```

The `Client` is your entry point to the API. All supported methods are available via properties on the created instance.

For example, to get a description of deal fields you can call the `crm.deal.fields` method:

```python
response = client.crm.deal.fields()
```

### Passing parameters in API calls

Most Bitrix24 REST API methods accept parameters. Pass them as positional or keyword arguments to the corresponding Python method.

To illustrate, we can get a deal by calling:

```python
response = client.crm.deal.get(bitrix_id=2)
```

### Retrieving results of the call

B24PySDK uses deferred method calls. To invoke a method and obtain its result, access the corresponding property.
The JSON response retrieved from the server is parsed into an object: `response.result` contains the value returned by the API method, while `response.time` provides the execution time of the request.

```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(domain="your_bitrix_portal", auth_token="key_of_your_webhook")
client = Client(bitrix_token)

response = client.crm.deal.update(bitrix_id=10, fields={'TITLE': 'New title'})
print(f'Updated successfully: {response.result}')
print(f'Call took {response.time.duration} seconds')
```

```text
Updated successfully: True
Call took 0.40396690368652344 seconds
```

### Retrieving records with list methods

For list methods, you can use `.as_list()` and `.as_list_fast()` to explicitly retrieve all records.
See documentation: [Handling large datasets](https://apidocs.bitrix24.com/api-reference/performance/huge-data.html)

By default, calling `.list()` returns up to 50 records only.

```python
response = client.crm.deal.list()
deals = response.result  # up to 50 records
```

The `.as_list()` method automatically retrieves all records.

```python
response = client.crm.deal.list()
deals = response.as_list().result  # full list of records
```

The `.as_list_fast()` method is optimized for large datasets.
It uses a more efficient algorithm and is recommended for receiving many records.

```python
response = client.crm.deal.list()
deals = response.as_list_fast().result  # generator
for deal in deals:  # requests are made lazily during iteration
    print(deal)
```

### Batch requests

You can execute multiple API calls in a single request using `call_batch`:

```python
from b24pysdk import Client, BitrixWebhook
bitrix_token = BitrixWebhook(domain="your_bitrix_portal", auth_token="key_of_your_webhook")
client = Client(bitrix_token)

batch = {
    'deal1': client.crm.deal.get(bitrix_id=1),
    'deal2': client.crm.deal.get(bitrix_id=2),
}
response = client.call_batch(batch)
for key, result in response.result.items():
    print(f"{key}: {result}")
```

### Multiple batches

For very large workloads you can send multiple batches sequentially via `call_batches`:

```python
requests = [
    client.crm.deal.get(bitrix_id=1),
    client.crm.deal.get(bitrix_id=2),
    # ...more requests
]
batches_response = client.call_batches(requests)
print(batches_response.result)
```

### Response metadata

List responses may include pagination metadata:

```python
resp = client.crm.deal.list()
print(resp.total)  # total number of records (if provided by API)
print(resp.next)   # next page offset (if provided by API)
```

### Configuration (timeouts and retries)

You can tweak default timeouts and retry behavior using `Config`:

```python
from b24pysdk import Config

cfg = Config()
cfg.default_timeout = 30            # seconds or (connect_timeout, read_timeout)
cfg.max_retries = 3                 # number of retries on transient errors
cfg.initial_retry_delay = 0.5       # seconds
cfg.retry_delay_increment = 0.5     # seconds
```

### Error handling

Common exceptions you may want to handle:

- `BitrixRequestError` / `BitrixTimeout`: network and timeout issues
- `BitrixAPIError`: API responded with an error (check `error` and `error_description`)
- `BitrixAPIExpiredToken`: access token expired; for `BitrixToken` B24PySDK can auto-refresh

```python
from b24pysdk.error import BitrixAPIError, BitrixTimeout

try:
    resp = client.crm.deal.get(bitrix_id=2)
    print(resp.result)
except BitrixTimeout:
    # retry or log
    pass
except BitrixAPIError as e:
    print(e.error, e.error_description)
```

## Library use via abstract classes

Instead of BitrixApp and BitrixToken, you can use their abstract class versions with frameworks and ORM libraries.
When using these abstract classes, the programmer is responsible for declaring the instance attributes and storing them.

Examples of the available abstract classes are AbstractBitrixApp, AbstractBitrixAppLocal, AbstractBitrixToken and AbstractBitrixTokenLocal.
