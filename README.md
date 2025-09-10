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

### Test environment (Docker-only, no local installs)

Local development and tests run inside Docker containers only. Nothing is installed to your host Python.

Two images are used:

- CI image: mirrors GitHub Actions, bakes sources; slower for iteration (rebuild on code change).
- Dev image: tools-only; build once, then run tests/lint against your working tree via bind mounts.

Common Makefile targets:

- Build dev image once: `make build-dev`
- Run unit tests (mounted repo, editable install): `make test`
- Run linter: `make lint`
- Optional shell in dev container: `make shell`

Notes:

- The repository is mounted at /work inside the container; sources are not copied into the image.
- If you add dependencies to `pyproject.toml`, `make test` reinstalls them in the container on next run.

### Tests overview

- Unit tests: fast, isolated; always run with `make test`.
- Integration tests: hit real Bitrix24 REST API; opt‑in and require credentials.

Run integration tests using one of the flows below.

1. Using an env file (.env.local preferred):

- Place credentials in `.env.local` (or `.env`). See `.env.example` template.
- Run: `make test-int` (auto-detects `.env.local` or `.env`, prints which is used).

2. Passing credentials via variables:

- Webhook: `make test-int-webhook B24_DOMAIN=... B24_WEBHOOK=...`
- OAuth: `make test-int-oauth B24_DOMAIN=... B24_CLIENT_ID=... B24_CLIENT_SECRET=... B24_ACCESS_TOKEN=...[ B24_REFRESH_TOKEN=...]`

Environment variables:

- Common
    - `B24_DOMAIN`: portal host only, e.g. `example.bitrix24.com` (no scheme). Helpers normalize/validate.
- Webhook
    - `B24_WEBHOOK`: incoming webhook in format `user_id/hook_key`.
- OAuth
    - `B24_CLIENT_ID`, `B24_CLIENT_SECRET`, `B24_ACCESS_TOKEN`, optional `B24_REFRESH_TOKEN`.

Behavior and skips:

- If credentials are missing, integration tests are skipped with a clear reason.
- The helpers will normalize `B24_DOMAIN` (strip scheme/slashes) and validate `B24_WEBHOOK`.

CI note:

- GitHub Actions runs linter and unit tests on push/PR (Python 3.9–3.12 matrix).
- Integration tests that call the real REST API do not auto‑run in CI.

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
from b24pysdk import BitrixWebhook

# For webhook URL: https://your_bitrix_portal.bitrix24.com/rest/1/key_of_your_webhook/
# Use domain without protocol and auth_token in format "your_user_id/key_of_your_webhook"
bitrix_token = BitrixWebhook(domain="your_bitrix_portal.bitrix24.com", auth_token="your_user_id/key_of_your_webhook")
```

2. Using a temporary OAuth 2.0 authorization token: <https://apidocs.bitrix24.com/api-reference/oauth/index.html>

For any type of apps:
```python
from b24pysdk import BitrixToken, BitrixApp

bitrix_app = BitrixApp(client_id="app_code", client_secret="app_key")

bitrix_token = BitrixToken(
    domain="your_bitrix_portal",
    auth_token="key_of_your_webhook",
    refresh_token="refresh_token_of_the_app",  # optional parameter
    bitrix_app=bitrix_app,
)
```

For local apps:
```python
from b24pysdk import BitrixTokenLocal, BitrixAppLocal

bitrix_app = BitrixAppLocal(
  domain="your_bitrix_portal", 
  client_id="app_code", 
  client_secret="app_key",
)

bitrix_token = BitrixTokenLocal(
    auth_token="key_of_your_webhook",
    refresh_token="refresh_token_of_the_app",  # optional parameter
    bitrix_app=bitrix_app,
)
```


The `Client` is your entry point to the API. All supported methods are available via properties on the created instance.
```python
from b24pysdk import Client

client = Client(bitrix_token)
```

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

bitrix_token = BitrixWebhook(domain="your_bitrix_portal.bitrix24.com", auth_token="your_user_id/key_of_your_webhook")
client = Client(bitrix_token)

request = client.crm.deal.update(bitrix_id=10, fields={"TITLE": "New title"})
print(f'Updated successfully: {request.result}')
print(f'Call took {request.time.duration} seconds')
```

```text
Updated successfully: True
Call took 0.40396690368652344 seconds
```

### Retrieving records with list methods

For list methods, you can use `.as_list()` and `.as_list_fast()` to explicitly retrieve all records.

See documentation: [Handling large datasets](https://apidocs.bitrix24.com/api-reference/performance/huge-data.html)

By default, list methods returns up to 50 records only.

```python
request = client.crm.deal.list()
deals = request.result  # up to 50 records
```

The `.as_list()` method automatically retrieves all records.

```python
request = client.crm.deal.list()
deals = request.as_list().result  # full list of records
```

The `.as_list_fast()` method is optimized for large datasets.
It uses a more efficient algorithm and is recommended for receiving many records.

```python
request = client.crm.deal.list()
deals = request.as_list_fast().result  # generator

for deal in deals:  # requests are made lazily during iteration
    print(deal["TITLE"])
```

### Batch requests

You can execute multiple API calls in a single request using `call_batch`:
> Method .call_batch() is used when you need to execute 50 or less API calls only.
```python
from b24pysdk import Client, BitrixWebhook

bitrix_token = BitrixWebhook(domain="your_bitrix_portal.bitrix24.com", auth_token="your_user_id/key_of_your_webhook")
client = Client(bitrix_token)

requests_data = {
    "deal1": client.crm.deal.get(bitrix_id=1),
    "deal2": client.crm.deal.get(bitrix_id=2),
    # ...more requests
}

batch_request = client.call_batch(requests_data)

for key, deal in batch_request.result.result.items():
    print(f"{key}: {deal['TITLE']}")
```

### Multiple batches

For very large workloads you can send multiple batches sequentially via `call_batches`:
> Method .call_batches() can execute more than 50 API calls.
```python
requests = [
    client.crm.deal.get(bitrix_id=1),
    client.crm.deal.get(bitrix_id=2),
    # ...more requests
]

batches_request = client.call_batches(requests)

for deal in batches_request.result.result:
    print(deal["TITLE"])
```

### Response metadata

List responses may include pagination metadata:

```python
request = client.crm.deal.list()
print(request.response.total)  # total number of records (if provided by API)
print(request.response.next)   # next page offset (if provided by API)
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
    request = client.crm.deal.get(bitrix_id=2)
    print(request.result)
except BitrixTimeout:
    # retry or log
    pass
except BitrixAPIError as e:
    print(e.error, e.error_description)
```

## Library use via abstract classes

Instead of BitrixApp and BitrixToken, you can use their abstract class versions with frameworks and ORM libraries.
When using these abstract classes, the programmer is responsible for declaring the instance attributes and storing them.

Examples of the available abstract classes are `AbstractBitrixApp`, `AbstractBitrixAppLocal`, `AbstractBitrixToken` and `AbstractBitrixTokenLocal`.
