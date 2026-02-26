from datetime import timedelta

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

## Migration from b24pysdk v0.1.0a1 to v0.2.0a1

If you started using the library with version 0.1.0a1, the following notes describe the key differences you need to account for when upgrading:

1. If you used `BitrixTimeout` or `BitrixOAuthTimeout`, make sure to update them to their new names — `BitrixRequestTimeout` and `BitrixOAuthRequestTimeout` respectively.
2. When using the Config class, you should now pass arguments with the `default_` prefix, such as `default_initial_retry_delay` or `default_max_retries`.
3. The `B24BoolStr` class has been removed from `b24pysdk.utils.types`. Use `B24BoolLit` from `b24pysdk.constants` instead.
4. The `B24BatchMethodTuple` help type has been added to `b24pysdk.utils.types` instead `B24BatchRequestData`.
5. The Requests and Responses classes are now available under the following paths:
   - `from b24pysdk.bitrix_api.requests import *`
   - `from b24pysdk.bitrix_api.responses import *`

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

- GitHub Actions runs linter and unit tests on push/PR (Python 3.9–3.14 matrix).
- Integration tests that call the real REST API do not auto‑run in CI.

## Library structure at a glance

- Client — entry point for all Bitrix24 calls: `client.crm`, `client.user`, `client.department`, `client.socialnetwork`.
- Authentication:
  - BitrixWebhook - incoming webhook auth
  - BitrixToken - OAuth 2.0 token auth (paired with BitrixApp)
  - BitrixApp - your Bitrix24 app credentials (client_id, client_secret)
- Responses expose `result` and `time` (including execution duration)

## Quickstart

This section provides a short guide to help you get started with B24PySDK.

### Calling an API method

To call the Bitrix24 API, import `Client` and use either `BitrixWebhook` or `BitrixToken` for authentication.
There are two ways to authenticate:

1. Using a permanent incoming local webhook code: <https://apidocs.bitrix24.com/local-integrations/local-webhooks.html>

```python
from b24pysdk import BitrixWebhook

# For webhook URL: https://example.bitrix24.com/rest/user_id/webhook_key/
# Use domain without protocol and auth_token in format "user_id/webhook_key"
bitrix_token = BitrixWebhook(domain="example.bitrix24.com", auth_token="user_id/webhook_key")
```

2. Using a temporary OAuth 2.0 authorization token: <https://apidocs.bitrix24.com/settings/oauth/index.html>

For any type of apps:
```python
from b24pysdk import BitrixToken, BitrixApp
from b24pysdk import Config
from datetime import timedelta

cfg = Config()

bitrix_app = BitrixApp(client_id="app_code", client_secret="app_key")

bitrix_token = BitrixToken(
    domain="example.bitrix24.com",
    auth_token="auth_token_of_the_app",
    refresh_token="refresh_token_of_the_app",  # optional parameter
    bitrix_app=bitrix_app,
    expires_in=3600,  # optional parameter
    expires=(Config().get_local_datetime() + timedelta(seconds=3600)) # optional parameter
)
```

For local apps:
```python
from b24pysdk import BitrixTokenLocal, BitrixAppLocal

bitrix_app = BitrixAppLocal(
  domain="example.bitrix24.com", 
  client_id="app_code", 
  client_secret="app_key",
)

bitrix_token = BitrixTokenLocal(
    auth_token="auth_token_of_the_app",
    refresh_token="refresh_token_of_the_app",  # optional parameter
    bitrix_app=bitrix_app,
)
```


#### Entry point
The `Client` class is the main entry point to the Bitrix API.
It acts as a factory that returns an API client instance depending on the selected Bitrix API version.
The factory hands back subclasses of `BaseClient`, which is the shared entry point for Bitrix calls.

Currently, Bitrix API supports multiple versions.
The latest version is v3. The SDK supports both v3 the previous one.

If the API version is not explicitly specified during client initialization, the SDK will use the default API version (currently v2).
```python
from b24pysdk import Client

client = Client(bitrix_token)
```
In this case, the client will be initialized with the default API version.

You can explicitly choose the Bitrix API version when creating the client:
```python
from b24pysdk import Client

client = Client(bitrix_token, prefer_version=3)
```

The way SDK methods are resolved depends on the selected preferred API version.

If you choose preferred API v3, the SDK works as follows:

- If a method exists in Bitrix API v3 and has a wrapper in the SDK, the SDK will use the v3 wrapper.
- If a method exists in Bitrix API v3 but does not have a v3-specific wrapper, the SDK will fall back to the wrapper from the previous API version (v2), if available.
- If a method exists in Bitrix API but does not have any wrapper in the SDK, it can still be called directly using BitrixToken.

This allows you to use API v3 immediately, even if not all methods have dedicated wrappers yet.

API v3 note: refresh token flow is not available yet, so the SDK cannot auto-refresh v3 access tokens. Use webhook auth or issue new OAuth tokens manually until Bitrix enables refresh for v3.

If API v2 is selected (explicitly or by default):
- Only wrappers for API v2 are available.

Wrappers implemented specifically for API v3 will not be accessible.


If you do not want to import Client you can use get_client() method and get Client instance from authenticator without writing import statement.

```python
from b24pysdk import BitrixToken, BitrixApp

bitrix_app = BitrixApp(client_id="app_code", client_secret="app_key")

bitrix_token = BitrixToken(
    domain="example.bitrix24.com",
    auth_token="auth_token_of_the_app",
    bitrix_app=bitrix_app,
)

client = bitrix_token.get_client()

request = client.crm.deal.update(bitrix_id=10, fields={"TITLE": "New title"})
print(f'Updated successfully: {request.result}')
```

For example, to get a description of deal fields you can call the `crm.deal.fields` method:

```python
request = client.crm.deal.fields()
```

### Passing parameters in API calls

Most Bitrix24 REST API methods accept parameters. Pass them as positional or keyword arguments to the corresponding Python method.

To illustrate, we can get a deal by calling:

```python
request = client.crm.deal.get(bitrix_id=2)
```

### Retrieving results of the call

B24PySDK uses deferred method calls. To invoke a method and obtain its result, access the corresponding property.
The JSON response retrieved from the server is parsed into an object: `response.result` contains the value returned by the API method, while `response.time` provides the execution time of the request.

```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(domain="example.bitrix24.com", auth_token="user_id/webhook_key")
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

bitrix_token = BitrixWebhook(domain="example.bitrix24.com", auth_token="user_id/webhook_key")
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
from b24pysdk.log import StreamLogger 
from datetime import timezone, timedelta

logger = StreamLogger()

cfg = Config()
cfg.configure(
    default_timeout=(3.05, 10),       # seconds or tuple (default_connection_timeout, default_read_timeout)
    default_max_retries=3,            # number of retries on transient errors
    default_initial_retry_delay=1,    # seconds
    default_retry_delay_increment=1,  # seconds
    logger=logger,                     
)

# other way to pass default timeout values
cfg.configure(
    default_connection_timeout=3.05,
    default_read_timeout=10,          # seconds or tuple (connect_timeout, read_timeout)
    default_max_retries=3,            # number of retries on transient errors
    default_initial_retry_delay=1,    # seconds
    default_retry_delay_increment=1,  # seconds
    logger=logger,                     
)
```

### Error handling

Common exceptions you may want to handle:

- `BitrixRequestError` / `BitrixRequestTimeout`: network and timeout issues
- `BitrixAPIError`: API responded with an error (check `error` and `error_description`)
- `BitrixAPIExpiredToken`: access token expired; for `BitrixToken` B24PySDK can auto-refresh

```python
from b24pysdk.error import BitrixAPIError, BitrixRequestTimeout

try:
    request = client.crm.deal.get(bitrix_id=2)
    print(request.result)
except BitrixRequestTimeout:
    # retry or log
    pass
except BitrixAPIError as e:
    print(e.error, e.error_description)
```

## Library use via abstract classes

Instead of BitrixApp and BitrixToken, you can use their abstract class versions with frameworks and ORM libraries.
When using these abstract classes, the programmer is responsible for declaring the instance attributes and storing them.

Examples of the available abstract classes are `AbstractBitrixApp`, `AbstractBitrixAppLocal`, `AbstractBitrixToken` and `AbstractBitrixTokenLocal`.

- AbstractBitrixApp: This class serves as the foundational blueprint for all Bitrix applications within the library. It outlines the essential credentials such as client_id and client_secret, which are crucial for authenticating applications with Bitrix24. By abstracting these components, it allows developers to focus on building their application logic while ensuring adherence to necessary authentication protocols.
- AbstractBitrixAppLocal: An extension of the AbstractBitrixApp, this class incorporates additional support specific to applications running within a predefined domain. This class is tailored to manage local instances of Bitrix applications, encapsulating both global application behavior and domain-specific settings, thereby streamlining application setup within a specific environment.
- AbstractBitrixToken: This class is designed to handle the complexities of managing authentication tokens for Bitrix24 API access. It provides a robust interface for ensuring tokens are current and valid, offering capabilities to automatically refresh them as needed. This abstraction allows for seamless API interaction; developers can make authenticated requests without delving into the intricacies of token lifecycle management.
- AbstractBitrixTokenLocal: Building on AbstractBitrixToken, this class adapts token management to work in tandem with local Bitrix applications. It ensures that token operations are tightly integrated with the domain-specific applications represented by AbstractBitrixAppLocal. The focus here is to facilitate a smooth, localized experience when managing authentication and interaction with Bitrix24 services, ensuring that both token and application settings are synchronized within a local context.


## Events subscription

Sometimes, when working with Bitrix24 through the SDK, it is necessary to react to internal changes within the client — for example, when an OAuth token expires and the SDK automatically obtains a new one, or when the Bitrix24 portal domain changes (which may happen if the portal is moved to another subdomain).

To handle such situations, the SDK provides an **event mechanism** that allows you to subscribe to and process specific events.

There are two key events you can listen to:

* **`OAuthTokenRenewedEvent`** — triggered when the authorization token (`access_token`) has been refreshed. This can be useful if you need to persist the new token in your database or logs.

* **`PortalDomainChangedEvent`** — triggered when the Bitrix24 portal domain has changed (for example, from `example.bitrix24.com` to `newexample.bitrix24.com`). This event can be used to update your application configuration or notify users about the domain change.

## Logging Utilities

The log module within the b24pysdk offers a suite of logging utilities designed to facilitate seamless integration with logging frameworks. It includes different logger implementations to cater to various logging needs:

- `AbstractLogger`: Defines the interface for all logger implementations, ensuring a consistent logging strategy across different modules.
- `BaseLogger`: Provides a fundamental implementation of the logging interface, offering a starting point for creating custom loggers.
- `NullLogger`: Implements a no-op logger that can be used in environments where logging is not required, effectively silencing all log outputs.
- `StreamLogger`: A concrete implementation for sending log outputs directly to the console or other stream handlers, useful for real-time log monitoring.


The logging utilities in b24pysdk enhance observability into API interactions, error tracking, and performance monitoring by offering detailed and configurable logging options. The modular design allows developers to customize and extend the logging functionalities as needed.

## Using Bitrix24 constants

For convenience use constant classes like EntityTypeAbbr or UserType from constants module.

```python
from b24pysdk.constants.crm import EntityTypeID

try:
    request = client.crm.item.fields(
        entity_type_id=EntityTypeID.DEAL,    # use constants for default CRM entities
        use_original_uf_names="N",
    ).result
    print(request["webformId"]["title"])
except BitrixAPIError as error:
    print(f"API Bitrix error {error.error: {error}}")
except Exception as error:
    print(f"Error: {error}")
```


## Validation classes

When working with received data from Bitrix24 you can use built-in validation. There are validation classes like:

1. `OAuthPlacementData` - app loading data validation when someone interact with you app or built-in;
2. `OAuthEventData` - validate event data from Bitrix24;
3. `OAuthWorkflowData` - workflow results validation.

With all validators above you should pass dictionary received from Bitrix24.

```python
from b24pysdk.credentials.oauth_placement_data import OAuthPlacementData

# get placement_data from Bitrix24

try:
    oauth_placement_data = OAuthPlacementData.from_dict(placement_data)
    print("OAuthPlacementData created successfully.")
    print(oauth_placement_data)
except OAuthPlacementData.ValidationError as e:
    print(f"Validation error: {e}")
```

