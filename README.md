# Bitrix24 REST API Python SDK

B24PySDK is the official Python SDK for the Bitrix24 REST API.

It provides typed Python wrappers around Bitrix24 REST methods, authentication helpers, lazy requests, pagination, batching, response schemas, runtime validation, retry handling, framework integrations, and optional SDK signals.

## Key features

- Incoming webhooks, OAuth applications, and local application credentials
- Automatic OAuth token refresh when a refresh token and app credentials are available
- Automatic portal-domain update after Bitrix24 redirects to a changed domain
- Typed Python wrappers for supported REST methods and parameters
- Runtime argument validation before an HTTP request is sent
- Lazy API requests with cached responses
- Raw API results through `.result`
- Python-friendly adapted results through `.value` and `.values`
- Typed schemas for structured Bitrix24 responses
- Standard pagination and optimized ID-based fast pagination
- Single-batch and automatic multi-batch execution
- Low-level `call_method()`, `call_list()`, `call_list_fast()`, `call_batch()`, and `call_batches()` helpers
- Configurable connect/read timeouts and retry behavior
- Automatic request IDs and SDK/Python version headers for diagnostics
- Secure logging with sensitive-value masking enabled by default
- Separate error models for REST API v1/v2 and v3
- Typed parsers for placement, event, and workflow callback payloads
- Validation of incoming OAuth payloads against Bitrix24 `app.info`
- Django, FastAPI, and Flask integrations
- Optional signals for OAuth token renewal and portal-domain changes
- Public SDK constants, enums, version metadata, and supported-method discovery
- ORM-like typed object layer with lazy object loading, query managers, relations, field metadata, local change tracking, and batch writes
- Extensible SDK objects and managers for portal-specific fields and application methods while preserving typed manager results

## Documentation

Bitrix24 REST API documentation: <https://apidocs.bitrix24.com/>

Project repository: <https://github.com/bitrix24/b24pysdk>

## Installation

B24PySDK requires Python 3.9 or newer.

```bash
pip install b24pysdk
```

Optional extras:

```bash
pip install "b24pysdk[signals]"
pip install "b24pysdk[django]"
pip install "b24pysdk[fastapi]"
pip install "b24pysdk[flask]"
```

The `signals` extra is needed only when subscribing to SDK signals. Regular REST calls and automatic OAuth token refresh do not require it.

## Quickstart

### Incoming webhook

For a webhook URL such as:

```text
https://example.bitrix24.com/rest/1/webhook_key/
```

use the portal domain without a protocol and pass the token as `user_id/webhook_key`:

```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(
    domain="example.bitrix24.com",
    webhook_token="1/webhook_key",
)

client = Client(bitrix_token)
```

### OAuth application

```python
from datetime import timedelta

from b24pysdk import BitrixApp, BitrixToken, Config, Client

bitrix_app = BitrixApp(
    client_id="app_code",
    client_secret="app_key",
)

bitrix_token = BitrixToken(
    domain="example.bitrix24.com",
    auth_token="access_token",
    refresh_token="refresh_token",  # optional
    bitrix_app=bitrix_app,
    expires_in=3600,  # optional
    expires=Config().get_local_datetime() + timedelta(seconds=3600),  # optional
)

client = Client(bitrix_token)
```

When a valid refresh token and `BitrixApp` are available, the SDK can refresh an expired OAuth token automatically.

### Local application

```python
from b24pysdk import BitrixAppLocal, BitrixTokenLocal, Client

bitrix_app = BitrixAppLocal(
    domain="example.bitrix24.com",
    client_id="app_code",
    client_secret="app_key",
)

bitrix_token = BitrixTokenLocal(
    auth_token="access_token",
    refresh_token="refresh_token",  # optional
    bitrix_app=bitrix_app,
)

client = Client(bitrix_token)
```

A client can also be obtained directly from a token:

```python
client = bitrix_token.get_client()
```

## OAuth token lifecycle

`BitrixApp` and OAuth-backed token objects expose helpers for the complete OAuth lifecycle.

Exchange an authorization code for a token:

```python
renewed_oauth = bitrix_app.get_oauth_token(code="authorization_code")

print(renewed_oauth.oauth_token.access_token)
print(renewed_oauth.oauth_token.refresh_token)
```

Refresh an existing token directly through the application:

```python
renewed_oauth = bitrix_app.refresh_oauth_token(
    refresh_token="refresh_token",
)
```

When a `BitrixToken` is bound to a `BitrixApp`, equivalent helpers are available on the token:

```python
renewed_oauth = bitrix_token.refresh_oauth_token()

# Refresh and replace auth_token / refresh_token / expiration data
# on the existing token object.
bitrix_token.refresh_and_set_oauth_token()
```

Useful token properties include:

- `bitrix_token.oauth_token` — current OAuth credentials as an `OAuthToken`
- `bitrix_token.has_expired` — whether the current access token is known to be expired
- `bitrix_token.is_one_off` — whether the token cannot be refreshed because it has no refresh token
- `bitrix_token.is_webhook` — whether the credentials represent an incoming webhook

Application installation information is available through `app.info`:

```python
app_info_response = bitrix_token.get_app_info()
app_info = app_info_response.result
```

You can also call it through the app object when you already have an access token:

```python
app_info_response = bitrix_app.get_app_info("access_token")
```

### Automatic expired-token recovery

For OAuth tokens with a refresh token and a bound `BitrixApp`, the SDK automatically refreshes an expired token before a request when expiration is known.

If Bitrix24 responds with an expired-token error, the SDK can refresh the token and retry the original request once. The refreshed credentials are written back to the `BitrixToken` instance.

This behavior applies to both high-level wrapped requests and low-level token calls.

### Automatic portal-domain changes

If a Bitrix24 portal domain changes and Bitrix24 redirects the API request to the new domain, the SDK can update `bitrix_token.domain` automatically and retry the request.

When the optional signals extra is installed, token renewal and portal-domain changes can also be observed through SDK signals. See [SDK signals](#sdk-signals).

## Client and API versions

`Client` is a factory that returns a client for the requested Bitrix REST API version.

The default preferred version is v2:

```python
from b24pysdk import Client

client = Client(bitrix_token)
```

You can explicitly request v1, v2, or v3:

```python
client_v1 = Client(bitrix_token, prefer_version=1)
client_v2 = Client(bitrix_token, prefer_version=2)
client_v3 = Client(bitrix_token, prefer_version=3)
```

When v3 is preferred, an individual REST method is sent to the v3 endpoint only if it is registered by the SDK as v3-capable. Other compatible calls fall back to the v2 transport behavior.

`ClientV3` also exposes v3-specific contexts such as `call`, `documentation`, `humanresources`, `mail`, `main`, `note`, `rest`, `tasks`, and `timeman`.

The set of methods treated as v3 methods can be inspected or overridden through `Config().api_v3_methods`:

```python
from b24pysdk import Config

print(Config().is_api_v3_method("example.method"))

Config().configure(
    api_v3_methods={
        "example.method",
        "another.method",
    },
)
```

Fast ID-based pagination is currently a v1/v2 feature; `call_list_fast()` / `.as_list_fast()` do not support API v3 methods.

## Calling wrapped REST methods

Scopes and methods follow the Bitrix24 REST hierarchy where practical:

```python
request = client.crm.deal.get(bitrix_id=2)
```

Another example:

```python
request = client.crm.deal.update(
    bitrix_id=10,
    fields={"TITLE": "New title"},
)

print(request.result)
```

B24PySDK request wrappers are lazy. Creating the request does not immediately perform the HTTP call. The request is executed on first access to properties such as `.response`, `.result`, `.time`, `.value`, or `.values`.

```python
request = client.crm.deal.get(bitrix_id=2)

# The HTTP request is performed here.
deal = request.result

# The converted response is cached and reused.
print(request.time.duration)
```

Calling `.call()` explicitly performs the request immediately and replaces the cached response with the new result:

```python
response = request.call()
print(response.result)
```

## Discovering supported SDK methods

You can inspect methods currently wrapped by the selected client:

```python
methods = client.get_supported_api_methods()
print(len(methods))
```

Limit discovery to a context:

```python
methods = client.get_supported_api_methods("crm.deal")
```

Or print them directly:

```python
client.print_supported_api_methods("crm")
```

## Calling methods without a wrapper

If a Bitrix24 REST method does not yet have an SDK wrapper, use the token directly.

### Single method

```python
response = bitrix_token.call_method(
    "crm.deal.get",
    {"id": 2},
)

print(response["result"])
```

### Paginated list

`call_list()` loads all pages for classic Bitrix24 v1/v2 list methods and returns a normal list in `response["result"]`:

```python
response = bitrix_token.call_list(
    "crm.deal.list",
    {
        "select": ["ID", "TITLE"],
        "filter": {"CLOSED": "N"},
    },
    limit=100,
)

for deal in response["result"]:
    print(deal["TITLE"])
```

### Fast list

`call_list_fast()` uses optimized ID-based pagination and returns a generator in `response["result"]`:

```python
response = bitrix_token.call_list_fast(
    "crm.deal.list",
    {
        "select": ["ID", "TITLE"],
        "filter": {"CLOSED": "N"},
    },
    limit=1000,
)

for deal in response["result"]:
    print(deal["TITLE"])
```

Do not pass `order`, `sort`, or `start` to `call_list_fast()` because the helper manages these parameters internally.

### Low-level batch

Low-level batch helpers accept `(method_name, params)` tuples:

```python
methods = {
    "deal1": ("crm.deal.get", {"id": 1}),
    "deal2": ("crm.deal.get", {"id": 2}),
}

response = bitrix_token.call_batch(methods)
print(response["result"]["result"])
```

Use `bitrix_token.call_batches()` when more than one Bitrix24 batch is required.

Low-level token calls execute immediately and return raw API-compatible dictionaries. High-level wrapper calls through `Client` return lazy SDK request objects.

All low-level token helpers still use the SDK authentication, timeout, retry, OAuth refresh, and portal-domain recovery behavior.

## Runtime type checking

SDK wrappers validate annotated method arguments at runtime before the request is executed. Invalid argument types and unsupported `Literal` values raise `TypeError` before an HTTP request is sent.

For example, if a wrapper expects an integer identifier, passing a string is rejected by the SDK:

```python
client.crm.deal.get(bitrix_id="2")  # TypeError
```

Use the wrapper signature and IDE type hints as the source of supported argument types and values.

## Responses

A regular SDK request exposes:

- `.response` — parsed response object
- `.result` — raw Bitrix24 `result`
- `.time` — Bitrix24 execution timing

Response objects can also be converted back to dictionaries with `.to_dict()`.

Timing information is represented by `BitrixTimeResponse` and includes Bitrix24 fields such as `start`, `finish`, `duration`, `processing`, `date_start`, `date_finish`, and optional operating-limit metadata when Bitrix24 returns it.

For regular responses, optional API pagination metadata is available through `.response.next` and `.response.total` when Bitrix24 returns it:

```python
request = client.crm.deal.list()

print(request.response.total)
print(request.response.next)
```

### Typed values and schemas

Some wrappers provide an adapter in addition to the raw result:

- `.result` keeps the raw Bitrix24-compatible value
- `.value` returns one Python-friendly adapted value
- `.values` returns a collection of adapted values

Schema classes are stored in `b24pysdk.schemas`.

```python
request = client.profile()

raw_profile = request.result
profile = request.value

print(raw_profile["ID"])
print(profile.bitrix_id)
```

For adapted list requests, `.result` remains raw while `.values` contains the adapted values.

Schemas represent Bitrix24 payloads using Python-friendly values. Schema classes expose `from_bitrix()` / `to_bitrix()` conversion where applicable, so the same model can be used to decode a Bitrix24 response and serialize data back to a Bitrix-compatible representation.

This schema layer is independent of the raw result: accessing `.value` or `.values` does not change what is available through `.result`.

## Lists and pagination

A normal Bitrix24 list call returns one API page, usually up to 50 records:

```python
request = client.crm.deal.list(
    select=["ID", "TITLE"],
    filter={"CLOSED": "N"},
    order={"ID": "ASC"},
)

deals = request.result
```

### `.as_list()`

Use `.as_list()` to retrieve all pages as one list:

```python
request = client.crm.deal.list().as_list()

deals = request.result
for deal in deals:
    print(deal["TITLE"])
```

An optional `limit` restricts the number of loaded items:

```python
request = client.crm.deal.list().as_list(limit=100)
```

`.as_list()` returns a flattened result after all required pages have been loaded. Its `.time` value contains timing aggregated across the pagination requests.

For requests with an adapter, use `.values`:

```python
request = some_typed_list_request.as_list()
values = request.values
```

### `.as_list_fast()`

Use `.as_list_fast()` for large datasets when the method supports ID-based fast pagination:

```python
request = client.crm.deal.list().as_list_fast()

for deal in request.result:
    print(deal["TITLE"])
```

The result is a one-time lazy generator. Additional pages are requested while the generator is consumed.

Because the request is lazy, fast-list timing is accumulated while the generator is being iterated. Final `.time` values are available after the generator has been fully consumed.

You can request descending traversal or apply a limit:

```python
request = client.crm.deal.list().as_list_fast(
    descending=True,
    limit=1000,
)
```

For adapted fast-list requests, `.values` is also a generator.

Fast pagination manages `order`, `sort`, and `start` internally. Do not set these parameters on the original request:

```python
request = client.crm.deal.list(
    select=["ID", "TITLE"],
    filter={"CLOSED": "N"},
).as_list_fast()
```

This mode is intended for methods that can be traversed reliably by an ID-like field and is currently available for API v1/v2 methods.

See Bitrix24 guidance on large datasets: <https://apidocs.bitrix24.com/api-reference/performance/huge-data.html>

## Batch requests

### One batch

`client.call_batch()` combines up to the SDK batch limit into one Bitrix24 batch request.

```python
requests = {
    "deal1": client.crm.deal.get(bitrix_id=1),
    "deal2": client.crm.deal.get(bitrix_id=2),
}

batch_request = client.call_batch(requests)

for key, deal in batch_request.result.result.items():
    print(key, deal)
```

A sequence can be used instead of a mapping:

```python
requests = [
    client.crm.deal.get(bitrix_id=1),
    client.crm.deal.get(bitrix_id=2),
]

batch_request = client.call_batch(requests)
```

Useful options include:

```python
batch_request = client.call_batch(
    requests,
    halt=True,
    ignore_size_limit=False,
)
```

### Multiple batches

For workloads larger than one batch, use `client.call_batches()`:

```python
requests = [
    client.crm.deal.get(bitrix_id=1),
    client.crm.deal.get(bitrix_id=2),
    # ...more requests
]

batches_request = client.call_batches(requests)

for deal in batches_request.result.result:
    print(deal)
```

Both batch helpers return lazy SDK request objects.

A batch result separates successful results and diagnostics:

```python
result = batch_request.result

print(result.result)        # successful command results
print(result.result_error)  # command errors
print(result.result_total)  # totals returned by list methods
print(result.result_next)   # next offsets returned by list methods
print(result.result_time)   # timing data for individual commands
```

When a mapping is passed to `call_batch()` / `call_batches()`, the same keys are preserved in the corresponding result mappings.

`halt=True` asks Bitrix24 to stop a batch after the first failed command. For a single batch, `ignore_size_limit=True` truncates an oversized command collection instead of raising an SDK size-limit error.

`client.call_batches()` automatically splits a larger request collection into multiple Bitrix24 batches and merges the returned result sections.

Low-level batch operations are also available from token objects through `call_batch()` and `call_batches()`.

## Configuration

`Config` stores thread-local runtime settings used by SDK requests. Different threads can therefore use different timeout, retry, logging, timezone, and API-version-routing settings.

```python
from b24pysdk import Config
from b24pysdk.log import StreamLogger

logger = StreamLogger()

Config().configure(
    default_timeout=(3.05, 10),
    default_max_retries=3,
    default_initial_retry_delay=1,
    default_retry_delay_increment=1,
    logger=logger,
    secure_log=True,
)
```

The default request settings are:

- connect timeout: `3.05` seconds
- read timeout: `10` seconds
- maximum request attempts: `3`
- initial retry delay: `1` second
- retry-delay increment: `1` second
- secure logging: enabled

You can configure connect and read timeouts separately:

```python
Config().configure(
    default_connect_timeout=3.05,
    default_read_timeout=10,
)
```

Request-level values can override global defaults:

```python
client = Client(
    bitrix_token,
    timeout=(3.05, 20),
    max_retries=2,
    initial_retry_delay=1,
    retry_delay_increment=2,
)
```

Individual wrapper requests can also accept supported request options through their method interface.

### Timezone handling

The SDK detects the local system timezone by default and falls back to UTC when it cannot be detected.

You can override it:

```python
from datetime import timezone

Config().configure(tz=timezone.utc)
```

Use SDK helpers when application code should follow the configured timezone:

```python
today = Config().get_local_date()
now = Config().get_local_datetime()
```

You can also inspect or configure the set of REST methods routed as API v3 through `Config().api_v3_methods`.

### Default client for the object layer

The object layer can resolve a client automatically through `Config().default_client_factory`.

For an application that works with one Bitrix24 portal:

```python
from b24pysdk import Config

Config().configure(
    default_client_factory=lambda: client,
)
```

After that, objects and managers can be used without `.using(client=...)` on every operation:

```python
from b24pysdk.objects.user import User

user = User(1)
print(user.name)

active_users = User.objects.filter(active=True).limit(20)
```

Configure a default object client only for a single-portal application. In a multi-portal application, bind the correct portal explicitly:

```python
users = User.objects.using(client=client).filter(active=True)
user = User(1, client=client)
```

A `client_factory` can also be supplied instead of an already constructed client. It is resolved lazily and the resolved client is reused by the provider that owns it.

## Reliability and request tracing

Temporary HTTP `503 Service Unavailable` responses are retried according to the configured retry policy. The delay starts at `default_initial_retry_delay` and increases by `default_retry_delay_increment` for subsequent retries.

OAuth-expiration recovery and portal-domain redirects are handled separately by the token layer, as described in [OAuth token lifecycle](#oauth-token-lifecycle).

Every outgoing REST request includes diagnostic headers with the SDK version, Python version, user agent, and an `X-Request-ID`.

The request ID is propagated from a supported environment variable when available (`REQUEST_ID`, `HTTP_X_REQUEST_ID`, or `UNIQUE_ID`); otherwise the SDK generates a UUID. This makes it possible to correlate application logs with outgoing Bitrix24 requests.

## Logging

The SDK provides logging abstractions in `b24pysdk.log`:

- `AbstractLogger` — logger interface
- `BaseLogger` — base implementation for custom loggers
- `NullLogger` — no-op logger used by default
- `StreamLogger` — stream/console logger

Example:

```python
from b24pysdk import Config
from b24pysdk.log import StreamLogger

Config().configure(
    logger=StreamLogger(),
    secure_log=True,
)
```

`secure_log=True` keeps sensitive values masked in SDK logs and is enabled by default. Disable it only in a controlled environment where sensitive log data cannot be exposed.

## Error handling

### REST API v1/v2

Common exceptions are available from `b24pysdk.errors`:

```python
from b24pysdk.errors import (
    BitrixAPIError,
    BitrixAPIBadRequest,
    BitrixAPIForbidden,
    BitrixAPIInternalServerError,
    BitrixAPINotFound,
    BitrixAPIServiceUnavailable,
    BitrixAPIUnauthorized,
    BitrixRequestTimeout,
)

try:
    deal = client.crm.deal.get(bitrix_id=9999).result
except BitrixRequestTimeout as error:
    print("Request timed out:", error)
except BitrixAPIUnauthorized as error:
    print("Unauthorized:", error)
except BitrixAPINotFound as error:
    print("Not found:", error)
except BitrixAPIForbidden as error:
    print("Forbidden:", error)
except BitrixAPIInternalServerError as error:
    print("Internal server error:", error)
except BitrixAPIServiceUnavailable as error:
    print("Service unavailable:", error)
except BitrixAPIBadRequest as error:
    print("Bad request:", error)
except BitrixAPIError as error:
    print(error.error, error.error_description)
```

Important base exceptions include:

- `BitrixSDKException`
- `BitrixValidationError`
- `BitrixRequestError`
- `BitrixRequestTimeout`
- `BitrixResponseError`
- `BitrixResponseJSONDecodeError`
- `BitrixAPIError`

Common Bitrix24 REST-specific subclasses include:

- `BitrixAPIExpiredToken` — the OAuth access token has expired
- `BitrixAPIInsufficientScope` — the token does not have enough permissions
- `BitrixAPITooManyRequests` — HTTP 429 / too many requests
- `BitrixAPIQueryLimitExceeded` — the REST request rate limit was exceeded
- `BitrixAPIOverloadLimit` — REST API is temporarily blocked because of portal/server overload

Catch these specific subclasses before their broader parent exceptions such as `BitrixAPIUnauthorized` or `BitrixAPIServiceUnavailable` when you need dedicated handling.

OAuth-specific exceptions are available from `b24pysdk.errors.oauth`.

### REST API v3

REST API v3 uses its own structured error payload. Import its error class from `b24pysdk.errors.v3`:

```python
from b24pysdk import Client
from b24pysdk.errors.v3 import BitrixAPIError

client = Client(bitrix_token, prefer_version=3)

try:
    task = client.tasks.task.get(bitrix_id=9999).result
except BitrixAPIError as error:
    print(error.code, error.error.message)

    if error.has_validation:
        for issue in error.validation or []:
            print(issue.field, issue.message)
```

## Constants

Bitrix24 constants are grouped under `b24pysdk.constants`.

For example:

```python
from b24pysdk.constants.crm import EntityTypeID

fields = client.crm.item.fields(
    entity_type_id=EntityTypeID.DEAL,
    use_original_uf_names="N",
).result
```

Prefer SDK constants and enums when they are available for a REST parameter.

## Object layer

`b24pysdk.objects` provides a higher-level, ORM-like interface over supported Bitrix24 entities.

It is built on the same typed REST scope wrappers and adds:

- typed Python objects backed by field descriptors;
- lazy loading of a single object by primary key;
- local unsaved changes and `save()`;
- immediate object `update()` / `delete()` where supported;
- typed, chainable object managers;
- filtering by SDK field names and Django-style lookup suffixes;
- ordering, selection, offsets, limits, and optimized fast loading where supported;
- typed object relations through `ObjectField`;
- `select_related()` bulk relation loading without an N+1 request pattern;
- field metadata, selectable values, and display values;
- batch creation, update, and delete;
- typed materialized `BitrixObjectList` collections;
- automatic REST-result adaptation to registered object classes;
- portal/application subclasses that can add custom fields and object methods;
- custom manager subclasses while preserving the concrete object type through manager chains and results.

The exact public methods of a concrete manager intentionally follow the capabilities of the underlying Bitrix24 REST endpoint. A manager does not expose an operation that its endpoint cannot support correctly.

### Available object families

The current object layer includes:

| Area | Objects | Main capabilities |
|---|---|---|
| Users | `User` | Lazy load, field metadata, user custom fields, URL, update/save; manager filter, `from_pks`, order, select, fast loading, add/batch add, batch update, admin mode, `current()`, `search()` |
| User custom-field definitions | `UserUserfield` | Lazy load, update/save/delete; manager filter, `from_pks`, order, add/batch add, batch update/delete |
| Departments | `Department` | Lazy load, field metadata, parent/head relations, update/save/delete; manager filter, `from_pks`, order, start, add/batch add, batch update/delete |
| Workgroups | `Workgroup` | Read/query model for `socialnetwork.api.workgroup`; filter, `from_pks`, order, select, `select_all`, start, endpoint `params` |
| Social-network groups/projects | `SonetGroup` | Update/save/delete plus owner/member/feature operations; manager filter, order, start, admin mode, add/batch add, batch update/delete |
| Event handlers | `Event`, `EventPK` | Composite-key registration objects, lazy load/delete, manager binding command through `add()` |
| Offline events | `OfflineEvent` | Query/filter/order/start/from-PK, reservation through `get()`, auth connector, immediate `clear()` / `error()` queue commands |
| Placements | `Placement`, `PlacementPK` | Composite-key registration objects, lazy load/delete, manager placement binding through `add()` |
| Universal lists | `List`, `ListElement`, `ListField`, `ListSection` | Typed list/list-element/list-field/list-section models, fixed list context, CRUD/batch operations where supported, custom `PROPERTY_*` fields, URLs, field metadata and file URL helpers |
| Business-process lists | `BitrixProcesses`, `BitrixProcessesElement`, `BitrixProcessesField`, `BitrixProcessesSection` | The same list object model specialized for business-process lists |
| Workgroup lists | `SocnetList`, `SocnetListElement`, `SocnetListField`, `SocnetListSection` | The same list object model specialized for social-network/workgroup lists |

Concrete classes are imported from their object modules:

```python
from b24pysdk.objects.department import Department
from b24pysdk.objects.user import User
from b24pysdk.objects.list import List
from b24pysdk.objects.list.element import ListElement
```

Reusable field descriptors, `BitrixObjectList`, batch result types, `BaseBitrixPK`, and `ClientProvider` are exported from `b24pysdk.objects`.

### Importing and registering object classes

Object classes are registered when Python creates the class, which normally happens when the module that defines it is imported.

Therefore an object implementation must be imported at least once in the current process before the SDK can resolve it through the object registry.

For direct object/manager usage this happens naturally:

```python
from b24pysdk.objects.user import User

users = User.objects.using(client=client).filter(active=True)
```

It matters most for application-specific overrides and for APIs that resolve objects dynamically by `OBJECT_KEY` / discriminator.

For example, if `myapp.bitrix_objects` defines:

```python
class ProjectElement(ListElement):
    IBLOCK_ID = 123
    ...
```

then import that module during application startup:

```python
import myapp.bitrix_objects  # registers ProjectElement
```

Do this **before** the first matching `.value` / `.values` adaptation or relation access.

Registration is process-wide. Importing the module a second time is not required.

This startup ordering is especially important for custom replacements:

- scope result adapters look up the currently registered class when adapting a REST result;
- string-based `ObjectField` relations resolve their registered class lazily and then cache that resolved class on the descriptor;
- importing an override only after such a relation was already resolved can therefore be too late for that already-cached relation descriptor.

For application-defined object overrides, the safest pattern is to import all custom object modules once during application initialization, before object-layer queries begin.

### Loading a single object

Constructing an object from its primary key does not make an HTTP request:

```python
from b24pysdk.objects.user import User

user = User(1, client=client)
```

The first read of a remote field loads the object:

```python
print(user.name)
```

Primary-key access itself does not load remote data:

```python
print(user.bitrix_pk)
print(user.bitrix_id)
```

An object can also be created from already available raw Bitrix24 data:

```python
user = User(
    bitrix_data={
        "ID": "1",
        "NAME": "John",
        "ACTIVE": "Y",
    },
    client=client,
)
```

Partial data is tracked explicitly. If a registered field was not present in a partial response, reading that field triggers one complete reload before the object decides that the field is really absent.

#### Data ownership and copying

When application code passes `bitrix_data` directly to an object constructor, the SDK performs a deep copy:

```python
raw_user = {
    "ID": "1",
    "NAME": "John",
    "CUSTOM_DATA": {
        "items": [1, 2, 3],
    },
}

user = User(
    bitrix_data=raw_user,
    client=client,
)

raw_user["CUSTOM_DATA"]["items"].append(4)

# The object is isolated from later mutations of raw_user.
```

The same defensive behavior is used by public `set_bitrix_data(...)` unless `copy_data=False` is explicitly requested.

Internal SDK adapters use a different ownership rule for performance. When a fresh REST response is adapted to SDK objects, the raw Bitrix24 dictionary is transferred to the object without another deep copy.

For example:

```python
request = client.user.get(
    filter={"ID": 1},
)

raw_users = request.result
users = request.values
```

For the standard `User` adapter, the dictionary used by `users[0]` is the same raw dictionary stored in `raw_users[0]`. Nested mutable values can therefore also be shared.

This is intentional: the SDK avoids copying a complete REST payload again when it already owns a fresh response.

Treat `.result` as read-only after adapting it through `.value` / `.values` if the adapted objects are still in use.

The public object snapshots remain defensive:

```python
snapshot = users[0].bitrix_data
snapshot["NAME"] = "Changed locally"

# users[0] is not modified.
```

`object.bitrix_data` and `object.local_data` always return detached deep-copied snapshots.

Concrete object classes expose entity-specific exception subclasses:

```python
try:
    print(User(999999, client=client).name)
except User.DoesNotExist:
    ...
```

`MultipleObjectsReturned` is exposed in the same way for object loaders that can receive more than one result unexpectedly.

### Object identity and primary keys

Every object exposes a normalized `bitrix_pk`.

Most object families use a scalar `int` or `str` key. Some Bitrix24 entities use typed composite keys; the SDK provides `BaseBitrixPK` plus concrete keys such as `EventPK` and `PlacementPK`.

Object equality requires both the same concrete Python class and the same primary key. Objects are hashable and can be used as dictionary keys; batch write results use object instances as keys.

### Client binding

Object operations can resolve a `Client` in three ways:

1. explicit `client=...`;
2. explicit `client_factory=...`;
3. `Config().default_client_factory`.

Manager binding:

```python
query = User.objects.using(client=client).filter(active=True)
```

Object binding:

```python
user = User(1).using(client=client)
```

`manager.using(...)` returns a new manager and does not modify the original manager. `object.using(...)` changes the client source for that object and returns the same object.

Objects created by one manager query share its client provider, so relation placeholders and later object operations continue to use the same portal.

For multi-portal applications, bind the client or factory explicitly for each portal instead of using a global default.

### Typed object fields

Object attributes are field descriptors that convert Bitrix24 wire values to Python values and convert assignments back to request-compatible values.

| Descriptor | Public value | Typical use |
|---|---|---|
| `IntField` | `int` | IDs, counters, integer values |
| `ListField` | `int` | ID of a portal-configured selectable value |
| `FloatField` | `float` | Decimal numeric values |
| `TextField` | `str` | Text |
| `HTMLField` | `str` | Bitrix24 `{TYPE, TEXT}` HTML-shaped values |
| `URLField` | `str` | Validated HTTP/HTTPS URLs |
| `BoolField` | `bool` | Bitrix24 boolean representations |
| `DateField` | `date` | Calendar dates |
| `DateTimeField` | `datetime` | Date/time values |
| `TimeField` | `time` | Time-of-day values |
| `TimeZoneField` | `ZoneInfo` | Timezone identifiers |
| `EnumField[E]` | enum `E` | Closed enum domains |
| `DictField` | `JSONDict` | JSON object values |
| `BitrixSchemaField[S]` | schema `S` | Typed nested SDK schemas |
| `AddressField` | `Address` | Bitrix24 addresses |
| `MoneyField` | `Money` | Bitrix24 money values |
| `FileField[F]` | file schema `F` | Remote/uploadable files |
| `ObjectField[O]` | object `O` | Relation stored through another field's primary key |
| `RawField` | `Any` | Opaque values with no stable typed contract |

Descriptors can additionally be required, multiple, read-only, add-only/not-updatable, or part of the primary key.

Multiple fields expose Python lists. Supported iterables, including generators, are materialized during conversion.

Assignment is local and makes no REST request:

```python
from datetime import date

user.name = "John"
user.personal_birthday = date(1990, 5, 10)

print(user.has_changes)
print(user.local_data)
```

Read-only and non-updatable fields reject invalid assignments before an API request is created.

### Raw state and local changes

For normal application code, prefer descriptor attributes such as `user.name`.

The object also exposes raw-state helpers:

```python
print(user.bitrix_data)  # detached raw snapshot + local changes
print(user.local_data)   # detached raw unsaved changes
print(user.has_changes)
```

Both dictionaries are detached snapshots; mutating them does not mutate the object.

Raw Bitrix24-code access is available for advanced cases:

```python
raw_name = user["NAME"]
user["NAME"] = "John"
```

Raw assignment bypasses public descriptor conversion, so descriptors are preferred.

Discard local changes without a request:

```python
user.reset_field("name")
user.reset_changes()
```

Reload remote data:

```python
user.refresh()
```

By default `refresh()` clears local changes. Preserve local changes over freshly loaded data with:

```python
user.refresh(clear_local_data=False)
```

### `update()` and `save()`

Where supported, `update()` sends an immediate write request:

```python
user.update(
    name="John",
    last_name="Smith",
)
```

Descriptor assignment plus `save()` provides a stateful workflow:

```python
user.name = "John"
user.last_name = "Smith"

user.save()
```

With no `update_fields`, `save()` sends **only fields recorded as local changes**. A clean object is a no-op:

```python
user.name = "John"
user.save()  # sends only NAME
```

`update_fields` changes that behavior. It contains SDK attribute names and sends the **current values of exactly those fields**, even when a field is not present in `local_data`:

```python
user.save(update_fields=["name", "last_name"])
```

This is useful for mutable field values that can be changed in place without invoking the descriptor setter.

For example, `UserUserfield.settings` is a `DictField`. Loaded dictionaries preserve their identity:

```python
from b24pysdk.objects.user.userfield import UserUserfield

userfield = UserUserfield(123, client=client)

settings = userfield.settings
settings["DEFAULT_VALUE"] = "new value"

print(userfield.has_changes)  # False

# Parameterless save() has no recorded setter change to send.
userfield.save()

# Explicitly send the current value of SETTINGS.
userfield.save(update_fields=["settings"])
```

The same rule is useful for other mutable values whose contents were changed in place without assigning the whole field again. For ordinary multiple descriptors, note that the public outer list is materialized during conversion; mutating that returned list does not automatically mean the object's raw stored list was changed.

When `update_fields` is supplied:

- names are SDK/Python attribute names, not raw Bitrix24 codes;
- selected fields do not have to be locally changed;
- a local unsaved value wins over the loaded remote value;
- otherwise the currently loaded raw value is sent;
- read-only or non-updatable fields are rejected;
- an explicitly empty `update_fields` iterable is invalid.

A successful write is merged back into the object's loaded state and the corresponding local changes are cleared.

Objects with a delete endpoint expose `delete()`:

```python
department.delete()
```

Not every object family supports every write operation; the public class surface follows the real REST API.

### Field metadata and `FieldAccessor`

Where Bitrix24 exposes entity field metadata, an object can resolve it through the current portal client:

```python
metadata = user.get_field("EMAIL")
title = user.get_field_title("EMAIL")
```

Metadata is cached per client/portal.

A bound field accessor is obtained by the **Python object attribute name**, not by the raw Bitrix24 field code:

```python
email = user.field("email")

print(email.value)
print(email.raw_value)
print(email.meta)
print(email.title)
```

For example, if an application object declares:

```python
status = ListField("PROPERTY_102")
```

then the accessor is:

```python
status_field = item.field("status")
```

not:

```python
item.field("PROPERTY_102")
```

The accessor exposes the descriptor together with one object instance and supports both reading and assignment through `.value` / `.raw_value`.

For `ListField`, the accessor can also expose portal-defined selectable items and human-readable values:

```python
status = item.field("status")

for choice in status.items:
    print(choice.bitrix_id, choice.value)

print(status.display_value)
```

`display_value` converts the stored Bitrix24 item ID to the corresponding human-readable value.

For a multiple `ListField`, it returns a list of display values in the same order as the selected IDs.

The conversion also works in the opposite direction. A display value can be assigned directly:

```python
item.field("status").display_value = "In progress"
item.save()
```

The accessor resolves `"In progress"` to the matching selectable item ID and assigns that ID through the ordinary field descriptor, so normal conversion, validation, local change tracking, and `save()` behavior are preserved.

For a multiple field:

```python
item.field("tags").display_value = [
    "Backend",
    "Priority",
]

item.save()
```

Setting `display_value = None` clears a scalar field. Setting an empty iterable on a multiple field clears it.

If the current field value is `None`, or a multiple field is empty, reading `display_value` returns immediately and does **not** load field metadata.

`items` / `display_value` require a `ListField` and an object family whose metadata source exposes selectable values.

#### Metadata caching for `.field(...)`, `.items`, and `.display_value`

Field metadata is not requested separately for every object.

The cache belongs to the current `Client`, so objects that use the same client and the same object metadata identity reuse the same loaded metadata.

For ordinary field managers the cache identity is based on:

```text
OBJECT_KEY + discriminator
```

For universal-list elements, field definitions are loaded as objects and cached for the concrete list discriminator. The effective cache identity is:

```text
"list.field" + (IBLOCK_TYPE_ID, IBLOCK_ID)
```

For example:

```python
class ProjectElement(ListElement):
    IBLOCK_ID = 123

    status = ListField("PROPERTY_102")
```

When iterating over many elements of list `123`:

```python
projects = (
    ProjectElement.objects
    .using(client=client)
    .limit(100)
    .to_list()
)

for project in projects:
    print(project.field("status").display_value)
```

the first accessor that actually needs selectable metadata causes the SDK to load the field definitions for list `123`.

For universal-list elements this is one `lists.field.get` request that returns the list's field definitions. The resulting field objects are stored in the client's object metadata cache.

The second and subsequent `ProjectElement` instances using the same `client` and the same `(IBLOCK_TYPE_ID, IBLOCK_ID)` reuse that cached field collection:

```text
project #1 -> lists.field.get -> cache fields for list 123
project #2 -> cached fields
project #3 -> cached fields
...
project #100 -> cached fields
```

So iterative access such as:

```python
for project in projects:
    print(project.field("status").title)
    print(project.field("status").items)
    print(project.field("status").display_value)
```

does **not** produce one field-metadata API request per project.

The same cache is reused by metadata-dependent accessor properties such as:

- `.meta`;
- `.title`;
- `.items`;
- `.display_value`.

A different list has a different discriminator and therefore a different metadata cache entry:

```python
class OtherProjectElement(ListElement):
    IBLOCK_ID = 456
```

The first metadata-dependent access for list `456` loads its own field definitions independently from list `123`.

Likewise, a different `Client` has its own cache. This is important for multi-portal applications because two portals can have different user fields, universal-list properties, titles, or selectable values.

Some object families also expose a class-level field manager:

```python
metadata = User.fields.using(client=client).list()
email_meta = User.fields.using(client=client).get("email")
```

Field managers are immediate metadata accessors, not lazy object query builders.

### Portal custom fields

Application subclasses can declare portal-specific fields while reusing the SDK object's loading, write, manager, metadata, relation, and batch behavior.

The SDK object families already identify their supported custom-field namespaces. Examples include:

- user fields: `UF_USR_*`;
- list-element properties: `PROPERTY_*`.

Choose the descriptor that matches the real Bitrix24 field type. A declared custom field can then participate in:

- object attribute reads and assignments;
- manager filters when the endpoint and descriptor support the lookup;
- `select()` / `select_all()` where the endpoint supports selection;
- object `update()` / `save()`;
- manager `add()` / `add_many()` through open custom-field dictionaries;
- field metadata and `FieldAccessor`;
- `ListField.items` and `display_value` for selectable properties.

A complete per-list extension example is shown below.

### File fields

`FileField[F]` exposes the concrete file schema used by that Bitrix24 field.

For URL-backed fields the SDK provides `URLFile` in `b24pysdk.schemas.file`. Local files can be created with:

```python
URLFile.from_bytes(...)
URLFile.from_base64(...)
URLFile.from_file(...)
URLFile.from_path(...)
```

File schemas expose:

```python
file.name
file.extension
file.is_local
file.read()
file.download()
file.open()
file.to_base64()
file.save_to(...)
```

Remote content is cached after the first download.

Universal-list element file properties use `ListElementFile`, because Bitrix24 returns property-value/file IDs instead of a direct URL:

```python
from b24pysdk.objects import FileField
from b24pysdk.objects.list.element import ListElement
from b24pysdk.schemas.list.field import ListElementFile


class MyListElement(ListElement):
    IBLOCK_ID = 123

    attachment = FileField[ListElementFile](
        "PROPERTY_104",
        file_class=ListElementFile,
    )
```

Create a local value and save it:

```python
item.attachment = ListElementFile.from_path("proposal.pdf")
item.save()
```

For a remote universal-list file, obtain the browser/download URLs through the element helper:

```python
urls = item.get_file_urls(field_id=104)
```

Use the actual Bitrix24 property ID for `field_id`.

### Relations and `ObjectField`

`ObjectField` projects a raw relation key as another SDK object.

For example, `Department` exposes both the raw head ID and the related `User`:

```python
department.uf_head_id
department.uf_head
```

Reading the relation does not immediately request the related row. It creates a lightweight related object containing its primary key and the same client provider. Reading a missing remote field on that related object can then load it lazily.

Assigning a related object updates the underlying relation key:

```python
department.uf_head = user
department.save()
```

Multiple relations return typed `BitrixObjectList` values.

### `select_related()` and avoiding N+1 requests

`ObjectField` is lazy by default.

Suppose `Department.uf_head` is backed by `Department.uf_head_id`.

After the parent department is loaded, reading:

```python
department.uf_head
```

does **not** immediately request the user from Bitrix24. The SDK creates a lightweight `User` object containing only that primary key and stores it in the `ObjectField` cache.

A later read such as:

```python
department.uf_head.name
```

can then load that one user lazily.

That behavior is convenient for occasional relation access, but iterating many parents and reading the relation on every row can create an N+1 pattern.

Use `select_related()` to preload supported relations in bulk.

#### Basic example

```python
from b24pysdk.objects.department import Department


departments = (
    Department.objects
    .using(client=client)
    .select_related(
        "parent",
        "uf_head.name",
        "uf_head.email",
    )
    .all()
)

for department in departments:
    if department.uf_head is not None:
        print(department.uf_head.name)
```

`select_related()` itself is a query modifier. For an unfiltered query, finish the chain with `.all()` before iteration.

#### Relation paths

A `select_related()` path must start with an `ObjectField`.

A path can end at the related object itself:

```python
select_related("uf_head")
```

or request ordinary fields on the related object:

```python
select_related(
    "uf_head.name",
    "uf_head.email",
)
```

Nested relations are supported:

```python
select_related(
    "parent.uf_head.name",
)
```

Every non-terminal path component must be an `ObjectField`.

The final component may be:

- another `ObjectField`, meaning "load this related object using its normal/default payload";
- an ordinary registered field, meaning "when loading the related object, request this field".

Invalid paths fail during query construction rather than silently falling back to per-object loading.

#### How the loader works

For every selected relation at the current level, evaluation performs the following steps.

1. **Load the parent objects.**

   The ordinary parent list query runs first.

2. **Make sure the relation source key is available.**

   `ObjectField` is backed by a real source field such as `UF_HEAD`, `PARENT`, or another ID field.

   If the parent query already returns a complete default payload, the SDK can use that value directly.

   If the parent query uses explicit `select(...)`, or the parent object type is incomplete without explicit selection, the relation source field is automatically added to the effective parent `select` list.

   Primary-key fields required to construct parent objects are also kept in the effective selection.

3. **Read relation placeholders from all parents.**

   Reading the `ObjectField` at this stage creates/caches lightweight related objects from the raw primary keys. It still does not issue one related-object request per parent.

4. **Collect unique related primary keys.**

   The SDK walks all parent objects, preserves first-seen key order, and removes duplicate related keys.

   If several departments reference the same head user, that user ID is loaded only once by this relation query.

5. **Create one bulk related-manager query for that `ObjectField`.**

   Conceptually the SDK performs:

   ```python
   RelatedObject.objects.using(client=client).from_pks(unique_pks).as_fast()
   ```

   The same `Client` is propagated from the parent manager.

   If the parent manager has an explicit timeout, the timeout is propagated to the related manager as well.

   This is one logical bulk relation query rather than one query per parent object. The lower API/list layer may still split a very large explicit-ID set into multiple REST requests when required by Bitrix24 limits.

6. **Apply terminal field selection.**

   If the path contains terminal fields:

   ```python
   select_related(
       "uf_head.name",
       "uf_head.email",
   )
   ```

   both paths are merged into the same relation tree, so `uf_head` is bulk-loaded once and the related `User` query receives the combined field selection.

   The related manager must expose public `select()` support when terminal fields need to be selected explicitly.

7. **Load nested relations recursively.**

   For:

   ```python
   select_related("parent.uf_head.name")
   ```

   the parent `Department` objects first bulk-load their `parent` departments.

   The nested `uf_head.name` relation tree is then passed to that related `Department` manager, which applies the same algorithm recursively.

8. **Index loaded related objects by primary key.**

   Returned related objects are placed into an in-memory primary-key index.

9. **Replace cached placeholders on the parents.**

   Each parent's cached `ObjectField` value is replaced with the loaded related object.

   Subsequent access:

   ```python
   department.uf_head
   department.uf_head.name
   ```

   uses that cached related object instead of loading the relation again.

#### Multiple relations

`ObjectField` can also be multiple.

For example, workgroup member relations can contain many `User` objects.

The loader:

- collects unique IDs across every parent and every item;
- bulk-loads each unique related primary key once for that selected relation;
- preserves the original per-parent list order;
- preserves duplicate relation entries in the parent's list;
- replaces each placeholder with the loaded object when a matching row was returned.

The public multiple relation remains a typed `BitrixObjectList`.

#### Missing related rows

A related primary key may exist in the parent response while the related bulk query no longer returns that row, for example because the related object was deleted or is inaccessible.

This is not treated as a fatal `select_related()` error.

The original primary-key-only placeholder remains in the parent's relation cache.

Accessing an unloaded field on that placeholder later follows the related object's normal lazy-loading behavior and can then raise its normal `DoesNotExist` error.

#### `select()` and `select_related()` are separate concepts

`select()` controls ordinary fields returned for an object.

`select_related()` controls which `ObjectField` relations are bulk-loaded.

They can be combined.

For example:

```python
departments = (
    Department.objects
    .using(client=client)
    .select(
        "bitrix_id",
        "name",
    )
    .select_related(
        "uf_head.name",
        "uf_head.email",
    )
    .all()
)
```

Even though the explicit parent `select()` does not mention `uf_head_id`, the SDK adds the relation source field required to preload `uf_head`.

Nested `select()` paths can also contribute the field selection used by a relation, but `select()` alone does not trigger relation loading. `select_related()` is the operation that performs the bulk relation query.

In normal application code, this is usually clearest:

```python
.select("bitrix_id", "name")
.select_related("uf_head.name", "uf_head.email")
.all()
```

#### Terminal relation versus terminal fields

These two queries are intentionally different:

```python
.select_related("uf_head")
```

and:

```python
.select_related("uf_head.name", "uf_head.email")
```

The first asks the related manager for its normal/default object payload.

The second asks it to select only the specified ordinary fields plus whatever primary-key fields the related object requires.

If a related object type is not complete without an explicit selection, loading only the relation itself can still produce a partial related object according to that endpoint's default response. Reading an omitted registered field later remains safe: the object can perform its ordinary complete lazy reload.

Specify terminal fields when you know exactly which related data will be consumed and want to avoid that later reload.

#### Request count characteristics

For a simple relation:

```python
Department.objects.select_related("uf_head").all()
```

the logical shape is:

```text
1 parent query
+ 1 bulk query for unique uf_head IDs
```

not:

```text
1 parent query
+ N user queries
```

For two different relations:

```python
.select_related(
    "parent",
    "uf_head",
)
```

the current loader performs one logical bulk query for `parent` and one logical bulk query for `uf_head` at that level.

For several terminal fields under the same relation:

```python
.select_related(
    "uf_head.name",
    "uf_head.email",
    "uf_head.work_position",
)
```

the paths are merged and `uf_head` is loaded once with the combined related selection.

For nested relations, each relation level is processed recursively after its parent level has been materialized.

#### Interaction with fast mode

`as_fast()` can normally expose a one-pass generator.

`select_related()` needs at least two passes over the parent result:

- one pass to collect related primary keys;
- another pass to replace/cache loaded related values.

Therefore, when `select_related()` is active, a fast parent stream is materialized into `BitrixObjectList` before relation loading.

Related objects themselves are loaded through their manager's `from_pks(...).as_fast()` path.

#### Requirements and errors

Bulk preloading is intentionally strict.

The related object's manager must provide a callable public `from_pks()` method.

If it does not, `select_related()` raises `BitrixObjectError` instead of silently making one REST request per related primary key.

When terminal related fields require explicit field selection, the related manager must also support public `select()`.

The parent manager may also need `select()` support when the effective parent request has to explicitly include relation source fields, for example when an explicit parent `select(...)` is already in use or the object API is incomplete without selection.

A relation that cannot be preloaded can still be used normally through lazy `ObjectField` access.

#### Client, cache, and query isolation

Related objects receive the same portal client as the parent manager.

The loaded related values are cached on the individual parent objects through the `ObjectField` descriptor.

They are **not** stored in a process-wide relation cache.

A separate manager clone represents a separate query and performs its own `select_related()` loading when evaluated.

This keeps relation results tied to the exact parent query and portal/client that produced them.


### Object managers

An object manager is a typed class-level descriptor and an immutable-style query builder.

Every manager access returns a fresh bound manager. Each chain method returns another manager, so query fragments do not mutate one another:

```python
base = User.objects.using(client=client).filter(active=True)

first_ten = base.limit(10)
first_hundred = base.limit(100)
```

The generic manager binding preserves the concrete object type. For a subclass `PortalUser(User)`, `PortalUser.objects.first()` is typed as `PortalUser | None`, while `PortalUser.objects.to_list()` is typed as `BitrixObjectList[PortalUser]`.

#### Common manager operations

All object managers inherit the following common behavior:

| Operation | Behavior |
|---|---|
| `.using(client=...)` / `.using(client_factory=...)` | Bind a portal/client source and return a new manager |
| `.timeout(value)` | Set the request timeout on the query |
| `.all()` | Mark the current query as an executable lazy result query |
| `.limit(n)` | Limit the logical number of returned objects |
| `.reverse()` | Reverse effective ordering |
| `.as_fast()` | Enable optimized one-pass fast loading |
| `.to_list()` | Materialize into `BitrixObjectList[T]` |
| `.count()` | Count matching objects; respects `limit`, ignores `start` |
| `.exists()` | Return whether at least one matching object exists |
| `.first()` | Return the first matching object or `None` |
| `.last()` | Reverse and return one object |
| `.select_related(...)` | Bulk-load supported object relations |

Concrete managers additionally expose only the endpoint-supported subset of:

- `filter(...)`;
- `from_pks(...)`;
- `order(...)`;
- `select(...)`;
- `select_all()`;
- `start(...)`;
- `add(...)`;
- `add_many(...)`;
- query-wide `update(...)`;
- query-wide `delete(...)`;
- endpoint-specific chain options such as `with_admin_mode()` / `with_params()`;
- endpoint-specific returning/command methods such as `current()`, `search()`, offline-event `get()`, `clear()`, and `error()`.

A bare class manager is a query builder, not an iterable result:

```python
users = User.objects.using(client=client)

# for user in users:
#     ...  # TypeError: manager has no result query
```

For normal application code, make the intent explicit in one of two ways:

```python
# Filtered result query
users = User.objects.using(client=client).filter(active=True)

# Unfiltered result query
users = User.objects.using(client=client).all()
```

After that, the manager can be iterated lazily.

Modifiers such as `order()`, `select()`, `select_related()`, `timeout()`, and `as_fast()` do not by themselves turn a fresh manager into a result query. Finish an unfiltered modifier-only chain with `.all()`:

```python
users = (
    User.objects
    .using(client=client)
    .select("bitrix_id", "name", "email")
    .order("name")
    .all()
)
```

`filter()` itself creates an executable result query, so no trailing `.all()` is needed:

```python
users = (
    User.objects
    .using(client=client)
    .filter(active=True)
    .select("bitrix_id", "name")
)
```

Internally, some other result-oriented operations such as `limit()`, `start()`, and `reverse()` also mark the manager as executable. For clear application code, prefer the simple rule: use `filter(...)` for a filtered query or `.all()` for an unfiltered query before iteration.

#### Filtering

Filters use SDK attribute names instead of raw Bitrix24 codes:

```python
users = User.objects.using(client=client).filter(
    active=True,
    name__contains="John",
)
```

Supported lookup suffixes are:

- `__ne`;
- `__gt`, `__gte`, `__lt`, `__lte`;
- `__in`, `__not_in`;
- `__contains`, `__like`, `__not_contains`, `__not_like`.

A lookup must be supported by both the descriptor type and the concrete object endpoint. Unsupported combinations raise `BitrixObjectFilterError` before the request is sent.

`bitrix_pk` is a synthetic filter name:

```python
user = User.objects.using(client=client).filter(bitrix_pk=1).first()

users = User.objects.using(client=client).filter(
    bitrix_pk__in=[1, 2, 3],
)
```

For a multiple field, passing an iterable without an explicit suffix is treated as an `IN` filter.

`from_pks()` is a bulk-ID convenience and uses one `IN` filter rather than one request per object:

```python
users = User.objects.using(client=client).from_pks([1, 2, 3])
```

The standard `from_pks()` is not exposed for composite-key managers unless their REST endpoint can express a real bulk composite-key query.

#### Ordering and reversal

Where supported, order by SDK field names:

```python
users = User.objects.using(client=client).order(
    "last_name",
    "name",
).all()
```

Prefix a name with `-` for descending order:

```python
users = User.objects.using(client=client).order("-name").all()
```

`reverse()` inverts the effective ordering. Some Bitrix24 endpoints impose stricter order formats and the concrete manager validates those restrictions.

#### Selecting fields

Where the REST endpoint supports selection:

```python
users = (
    User.objects
    .using(client=client)
    .select("name", "email")
    .limit(100)
    .all()
)
```

Selections use SDK attribute names. Required primary-key fields are added automatically so every returned row remains a valid object.

Select all registered fields:

```python
users = User.objects.using(client=client).select_all().all()
```

Partial objects remain safe: if application code later reads a registered field that was not selected, the object performs one complete lazy reload before returning it. Therefore `select()` is most useful when omitted fields will not be read later.

#### Pagination, limits, count, and length

Where supported, `start()` sets the Bitrix24 page offset:

```python
users = User.objects.using(client=client).start(100)
```

`limit()` caps the logical result across pagination:

```python
users = User.objects.using(client=client).filter(active=True).limit(200)
```

`count()` uses the API `total` when available and otherwise falls back to returned values. It respects `limit`, intentionally ignores `start`, and logs a warning when an existing `start` is removed for counting:

```python
count = User.objects.using(client=client).filter(active=True).count()
```

For a normal manager, `len(manager)` delegates to `count()` until that manager already owns a materialized `BitrixObjectList`; then it returns the in-memory length without another request.

For a non-materialized fast manager, `len()` raises `TypeError`. Use `count()` explicitly or call `to_list()` first.

#### Fast loading

Enable optimized primary-key traversal with:

```python
users = (
    User.objects
    .using(client=client)
    .filter(active=True)
    .as_fast()
)

for user in users:
    ...
```

Fast mode can expose a one-pass generator.

Restrictions:

- it cannot be combined with `start`;
- explicit ordering, if present, must contain the complete primary key;
- all primary-key components must use one direction;
- non-PK or mixed-direction order is rejected;
- `len()` is unavailable until the fast result is materialized.

Materialize when the data must be reused:

```python
users = users.to_list()
```

`select_related()` also materializes a fast parent stream when relation preloading needs multiple passes.

#### Query evaluation and caching

Manager queries are lazy:

```python
query = User.objects.using(client=client).filter(active=True)

# The list request is made here.
for user in query:
    ...
```

A normal evaluated query caches its `BitrixObjectList`, so iterating that same manager again does not repeat the list request.

A fast query may cache a one-pass generator. Use `to_list()` when the same result must be consumed more than once.

A newly chained manager is a separate query and does not share the evaluated response cache of its parent manager.

Membership materializes the current query:

```python
if user in User.objects.using(client=client).filter(active=True):
    ...
```

### Creation and batch creation

Where supported, `add()` returns the manager's concrete object type:

```python
from b24pysdk.objects.department import Department


department = Department.objects.using(client=client).add(
    name="Development",
    sort=100,
)
```

Managers with bulk creation expose `add_many()`:

```python
result = Department.objects.using(client=client).add_many([
    {"name": "Backend", "sort": 100},
    {"name": "Frontend", "sort": 200},
])

for department in result.results:
    print(department.bitrix_pk)

print(result.errors)
print(result.is_success)
print(result.has_errors)
```

`add_many()` accepts either a sequence of SDK-field dictionaries or a mapping of caller-defined keys to field dictionaries.

It returns `BitrixObjectBatchAddResult[T]`.

The result exposes:

```python
result.results     # BitrixObjectList[T] of created objects
result.errors      # {input_key_or_index: raw_api_error}

result.is_success  # True when errors is empty
result.has_errors  # bool(result.errors)
```

For a sequence input, failed items are keyed by their original **zero-based input index**:

```python
result = Department.objects.using(client=client).add_many([
    {"name": "Backend", "sort": 100},
    {"name": "Frontend", "sort": 200},
])

for index, error in result.errors.items():
    print("Failed input index:", index, error)
```

For a mapping input, failed items keep the caller-defined mapping key:

```python
result = Department.objects.using(client=client).add_many({
    "backend": {"name": "Backend", "sort": 100},
    "frontend": {"name": "Frontend", "sort": 200},
})

if "backend" in result.errors:
    print(result.errors["backend"])
```

Successful add results are converted to concrete typed SDK objects and collected in `result.results`. Caller keys are intentionally preserved only for errors; `result.results` is an object list rather than a success mapping.

For a custom object manager, the type parameter is preserved:

```python
# BitrixObjectBatchAddResult[ProjectElement]
result = ProjectElement.objects.using(client=client).add_many([...])

# BitrixObjectList[ProjectElement]
created = result.results
```

Empty input returns:

```python
result.results == []
result.errors == {}
result.is_success is True
```

without a REST request.

### Query-wide batch update and delete

When exposed by the concrete manager, `update()` and `delete()` operate on all objects in the current query and use the SDK batch API:

```python
result = (
    Department.objects
    .using(client=client)
    .filter(name__contains="Old")
    .update(name="Renamed")
)
```

Manager `update()` receives SDK attribute names and applies descriptor conversion.

Delete matching objects:

```python
result = (
    Department.objects
    .using(client=client)
    .filter(bitrix_pk__in=[10, 11, 12])
    .delete()
)
```

Query-wide manager writes and `BitrixObjectList.update()` / `.delete()` return `BitrixObjectBatchWriteResult[T]`.

It keeps both the raw per-object batch result and convenient object lists:

```python
result.result
# {object: success_result}

result.result_error
# {object: raw_api_error}

result.results
# BitrixObjectList[T] containing keys from result.result

result.errors
# BitrixObjectList[T] containing keys from result.result_error

result.is_success
# not result.has_errors

result.has_errors
# bool(result.result_error)
```

The dictionaries are keyed by the actual SDK object instances:

```python
for department, value in result.result.items():
    print(department.bitrix_pk, value)

for department, error in result.result_error.items():
    print(department.bitrix_pk, error)
```

For batch updates, numeric Bitrix24 success values are normalized to `bool` before they are stored in `result.result`.

`result.results` and `result.errors` are fresh typed `BitrixObjectList` views over the corresponding dictionary keys and preserve the list-level client provider used for the batch operation.

For `BitrixObjectList.update()` with no explicit raw payload, objects with no local changes are skipped completely; skipped objects are absent from both `result.result` and `result.result_error`.

An empty target set returns an empty successful `BitrixObjectBatchWriteResult` without a REST batch call.

### `BitrixObjectList`

`to_list()` returns a typed `BitrixObjectList[T]`, a normal Python list with object-layer helpers:

```python
users = (
    User.objects
    .using(client=client)
    .filter(active=True)
    .limit(100)
    .to_list()
)

print(users.length)
print(users.exists())
print(users.first())
print(users.last())
print(users.to_pks())
```

Slicing and `.copy()` preserve the `BitrixObjectList` type and its list-level client provider.

Batch-save each contained object's local changes:

```python
for user in users:
    user.title = "Developer"

result = users.update()
```

Objects without local changes are skipped.

A raw Bitrix24-code payload can intentionally be applied to every object:

```python
result = users.update({
    "ACTIVE": "N",
})
```

This `BitrixObjectList.update(mapping)` overload uses raw Bitrix24 field codes, unlike manager `update(**fields)`, which uses SDK attribute names.

Delete all contained objects where supported:

```python
result = users.delete()
```

Bind a client specifically for list-level batch operations:

```python
users.using(client=client)
```

This does not replace the client providers already stored in the contained objects.

### Object-specific operations

Objects and managers can expose domain operations that do not fit generic CRUD.

Examples:

```python
current_user = User.objects.using(client=client).current()

found_users = User.objects.using(client=client).search(
    name="John",
    last_name="Smith",
)
```

`SonetGroup` objects additionally expose:

- `set_owner()`;
- `invite_users()`;
- `request_join()`;
- `add_users()`;
- `update_users_role()`;
- `get_members()`;
- `remove_users()`;
- `feature_access()`.

Offline-event managers expose queue-specific operations in addition to ordinary list queries:

```python
from b24pysdk.objects.event.offline import OfflineEvent


events = (
    OfflineEvent.objects
    .using(client=client)
    .with_auth_connector("connector")
    .get(limit=50)
)

OfflineEvent.objects.using(client=client).clear(process_id)
OfflineEvent.objects.using(client=client).error(process_id)
```

`Event.objects.add()` and `Placement.objects.add()` are binding commands and return a success flag because those APIs do not return enough information to construct the registered composite-key object immediately.

### Universal lists and fixed list context

The list element, field, and section families use a discriminator to represent both list type and concrete list ID.

`ListElement` fixes the universal-list type:

```python
IBLOCK_TYPE_ID = ListIBlockType.LISTS
```

but the generic class does not know the ID of a concrete portal list:

```python
IBLOCK_ID = None
```

Application code working with one known list should subclass the object and set `IBLOCK_ID`. The fixed list type and ID are then automatically added to its single-object loads and ordinary manager list/filter/add/update/delete requests.

The same pattern is used for list fields and sections. Separate class families exist for universal lists, business-process lists, and social-network/workgroup lists.

### Extending objects for one portal list

Assume a portal administrator created a universal list with:

```text
IBLOCK_ID = 123
```

and the list has these custom properties:

```text
PROPERTY_101  Customer          text
PROPERTY_102  Status            list/select
PROPERTY_103  Budget            number
PROPERTY_104  Attachment        file
```

Replace these example codes with the real property codes from the target portal.

#### Variant 1: extend only the object

Subclass `ListElement`, fix `IBLOCK_ID`, add typed field descriptors, and add application methods if needed:

```python
from b24pysdk.objects import FileField, FloatField, ListField, TextField
from b24pysdk.objects.list.element import ListElement
from b24pysdk.schemas.list.field import ListElementFile


class ProjectElement(ListElement):
    IBLOCK_ID = 123

    customer = TextField("PROPERTY_101")
    status = ListField("PROPERTY_102")
    budget = FloatField("PROPERTY_103")
    attachment = FileField[ListElementFile](
        "PROPERTY_104",
        file_class=ListElementFile,
    )

    def customer_label(self) -> str:
        return f"{self.name}: {self.customer or '-'}"
```

No manager override is required. The inherited `ListElement.objects` descriptor binds itself to `ProjectElement` and keeps the concrete object type in manager results:

```python
project = (
    ProjectElement.objects
    .using(client=client)
    .filter(status=7)
    .select(
        "bitrix_id",
        "name",
        "customer",
        "status",
        "budget",
    )
    .first()
)

# Static type: ProjectElement | None
```

Materialized results keep the same type parameter:

```python
projects = (
    ProjectElement.objects
    .using(client=client)
    .filter(status=7)
    .to_list()
)

# Static type: BitrixObjectList[ProjectElement]
```

Creation also returns the subclass:

```python
created = ProjectElement.objects.using(client=client).add(
    element_code="PROJECT-001",
    name="New project",
    customer="Acme",
    status=7,
    budget=150000.0,
)

# Static type: ProjectElement
```

The inherited `add()` accepts application fields through `**fields`; descriptor conversion still validates/converts them at runtime. If application code also needs IDE-visible typed manager arguments or named application query methods, extend the manager too.

A direct reference uses the same fixed list context:

```python
project = ProjectElement(500, client=client)

print(project.name)
print(project.url)
```

Selectable custom properties integrate with `FieldAccessor`:

```python
print(project.field("status").display_value)

project.field("status").display_value = "In progress"
project.save()
```

A file property uses the matching file schema:

```python
project.attachment = ListElementFile.from_path("proposal.pdf")
project.save()

urls = project.get_file_urls(field_id=104)
```

#### Variant 2: extend the object and the manager

This is an **alternative complete definition** to Variant 1, not a second class definition to execute after Variant 1.

If `ProjectElement` from Variant 1 has already been imported and registered for the same `(OBJECT_KEY, discriminator)`, do not redefine another unrelated `ProjectElement` directly from `ListElement`; the registry intentionally requires a replacement for the same key/discriminator to inherit the currently registered class.

When application code needs custom typed manager methods from the start, the usual portal-specific case does **not** need another `Generic` / `TypeVar` layer.

Specialize `ListElementManager` once with the concrete application object.

Because the manager class is declared before the object class, use a forward reference in the generic argument:

```python
from b24pysdk.objects import FileField, FloatField, ListField, TextField
from b24pysdk.objects.list.element import ListElement, ListElementManager
from b24pysdk.schemas.list.field import ListElementFile


class ProjectElementManager(ListElementManager["ProjectElement"]):
    def with_status(
        self,
        status_id: int,
    ) -> "ProjectElementManager":
        return self.filter(status=status_id)

    def create_project(
        self,
        *,
        code: str,
        name: str,
        customer: str,
        status_id: int,
        budget: float,
    ) -> "ProjectElement":
        return self.add(
            element_code=code,
            name=name,
            customer=customer,
            status=status_id,
            budget=budget,
        )


class ProjectElement(ListElement):
    IBLOCK_ID = 123

    objects: "ProjectElementManager" = ProjectElementManager()

    customer = TextField("PROPERTY_101")
    status = ListField("PROPERTY_102")
    budget = FloatField("PROPERTY_103")
    attachment = FileField[ListElementFile](
        "PROPERTY_104",
        file_class=ListElementFile,
    )

    def customer_label(self) -> str:
        return f"{self.name}: {self.customer or '-'}"
```

The base manager is now specialized directly as:

```text
ListElementManager[ProjectElement]
```

so inherited manager operations keep the concrete application type without making `ProjectElementManager` itself generic.

For example:

```python
query = (
    ProjectElement.objects
    .using(client=client)
    .with_status(7)
    .limit(20)
)

# Static manager type:
# ProjectElementManager

project = query.first()

# Static result type:
# ProjectElement | None
```

Custom typed creation also returns the same object type:

```python
project = ProjectElement.objects.using(client=client).create_project(
    code="PROJECT-002",
    name="Typed project",
    customer="Acme",
    status_id=7,
    budget=250000.0,
)

# Static type: ProjectElement
```

Inherited manager methods remain typed too:

```python
projects = (
    ProjectElement.objects
    .using(client=client)
    .from_pks([500, 501, 502])
    .select("name", "customer", "status")
    .to_list()
)

# Static type: BitrixObjectList[ProjectElement]
```

And batch-add results keep the same parameter:

```python
result = ProjectElement.objects.using(client=client).add_many([
    {
        "element_code": "PROJECT-003",
        "name": "Another project",
        "customer": "Acme",
        "status": 7,
        "budget": 100000.0,
    },
])

# Static type:
# BitrixObjectBatchAddResult[ProjectElement]

created = result.results

# Static type:
# BitrixObjectList[ProjectElement]
```

Use a generic custom manager only when you deliberately plan to subclass the application object again **and** want that further subtype to flow through the same custom manager class. For the usual "one concrete portal list -> one application object" model, the concrete specialization above is simpler and keeps the desired typing.

This pattern allows application code to add both portal-specific object fields/methods and manager-specific typed query/command methods without losing result typing for `first()`, `last()`, `add()`, `to_list()`, `add_many()`, or batch result objects.


#### Automatic object registration and discriminators

No manual registration call is needed for normal subclassing. Creating a `BaseObject` subclass registers it automatically under its inherited object key and its discriminator.

For the example above:

```text
object key:     list.element
discriminator:  (lists, 123)
class:          ProjectElement
```

The list-element discriminator is:

```text
(IBLOCK_TYPE_ID, IBLOCK_ID)
```

Resolution is most-specific first. Conceptually, for universal list `123`:

```text
(lists, 123)
(lists, None)
(None, None)
None
```

Therefore setting only `IBLOCK_ID = 123` customizes one concrete universal list without replacing the SDK model for every other list.

If another class later replaces exactly the same `(object key, discriminator)` registration, it must inherit the class currently registered for that pair.

Remember that registration happens only when the module containing the subclass is imported. Import application object modules during startup before the first matching object adaptation or relation resolution.

Supported REST adapters resolve the currently registered runtime class too. After the custom class is imported/defined, a matching generic REST call such as:

```python
request = client.lists.element.get(
    "lists",
    iblock_id=123,
)
```

adapts matching values to the currently registered runtime class for `(lists, 123)`.

A generic scope method cannot statically infer an application class from a runtime `iblock_id`, so its declared response type remains the SDK base object. Use the custom object's manager as the typed application entry point when static subtype inference matters.

#### Important update rule for list `PROPERTY_*` fields

`lists.element.update` can clear values omitted from the full outgoing element payload.

The object layer therefore preserves existing ordinary values before updating. For `PROPERTY_*` values it also requires every current custom property returned by Bitrix24 to be declared on the concrete object class.

If the API returns an undeclared `PROPERTY_*`, `update()` / `save()` raises `BitrixObjectFieldError` asking you to declare it before the write.

For a concrete portal list that application code updates:

- declare all custom `PROPERTY_*` fields returned for its elements;
- use the descriptor matching each Bitrix24 property type;
- do this before object or manager update operations.

This prevents an update to one custom property from accidentally clearing another portal-defined property.

### Extending other SDK objects

The same application-subclass model is not limited to lists.

For example, a portal-specific user field can be added by subclassing `User`:

```python
from b24pysdk.objects import TextField
from b24pysdk.objects.user import User


class PortalUser(User):
    crm_code = TextField("UF_USR_CRM_CODE")

    def crm_label(self) -> str:
        return f"{self.bitrix_id}:{self.crm_code or '-'}"
```

The inherited manager binds to the subclass:

```python
users = (
    PortalUser.objects
    .using(client=client)
    .filter(crm_code="A-100")
    .to_list()
)

# Static type: BitrixObjectList[PortalUser]
```

Add a custom manager when application-specific manager methods/signatures are needed. For a fixed application class, specialize the SDK manager directly with that concrete object type; use an additional generic manager layer only when further subclassing is intentional.

### Object metadata caches

Field metadata is portal-specific and is cached on the `Client`.

Standard field managers use the client field cache keyed by the object's `OBJECT_KEY` and discriminator.

Object-backed metadata, including user custom-field definitions and universal-list field definitions, is loaded as a **complete collection** and cached by object family/discriminator. This is why iterating over many objects and repeatedly using `.field(...)`, `.title`, `.items`, or `.display_value` does not normally create an N+1 metadata-query pattern.

For universal-list elements, one concrete list has one cached field collection per client:

```text
("list.field", (IBLOCK_TYPE_ID, IBLOCK_ID))
```

This means:

- the first metadata-dependent access can load all field definitions for that object family/list;
- later objects of the same family/discriminator reuse the same cached collection;
- repeated field title/item/display-value access does not request each field or each object independently;
- separate clients keep separate portal metadata;
- different concrete lists keep independent list-field metadata;
- custom-field definitions and selectable values can safely differ between portals and list IDs;
- reading `display_value` for `None` or an empty multiple value does not load metadata at all.

### Object-layer errors

Object-layer exceptions are available from `b24pysdk.objects.errors`:

- `BitrixObjectError`;
- `BitrixObjectDoesNotExist`;
- `BitrixObjectMultipleObjectsReturned`;
- `BitrixObjectClientError`;
- `BitrixObjectFieldError`;
- `BitrixObjectFilterError`;
- `BitrixObjectFieldReadOnlyError`;
- `BitrixObjectFieldNotLoadedError`.

Concrete object classes also expose their own `DoesNotExist` and `MultipleObjectsReturned` subclasses for entity-specific exception handling.


## Incoming payload validation

The credentials package contains typed parsers for common Bitrix24 callback payloads:

- `OAuthPlacementData` — placement launch data
- `OAuthEventData` — event callback data
- `OAuthWorkflowData` — workflow robot callback data
- `OAuth`, `EventOAuth`, `WorkflowOAuth`, and `RenewedOAuth` — typed OAuth/auth payload models used by incoming Bitrix24 data and token renewal flows

Example:

```python
from b24pysdk.credentials import OAuthPlacementData

try:
    placement = OAuthPlacementData.from_dict(placement_data)
    print(placement.domain)
except OAuthPlacementData.ValidationError as error:
    print("Validation error:", error)
```

Token objects can also be constructed from parsed OAuth payloads:

```python
from b24pysdk import BitrixToken

bitrix_token = BitrixToken.from_oauth_placement_data(
    placement,
    bitrix_app,
)
```

Equivalent token constructors are available for other incoming OAuth payloads:

```python
bitrix_token = BitrixToken.from_oauth(oauth, bitrix_app)
bitrix_token = BitrixToken.from_oauth_event_data(event_data, bitrix_app)
bitrix_token = BitrixToken.from_oauth_workflow_data(workflow_data, bitrix_app)
```

Equivalent constructors are available on `BitrixTokenLocal` for local applications.

The callback models accept flattened request keys used by Bitrix24 webhooks/forms and normalize them into typed Python structures.

Common helpers include:

- `.to_dict()` — convert parsed callback data back to a dictionary
- `.get_app_info(bitrix_app)` — load and cache Bitrix24 `app.info` for the payload when the callback contains usable OAuth context
- `.validate_against_app_info(app_info)` — verify that installation/member/domain/user data match the expected app installation

For event callbacks, `OAuthEventData.is_system` indicates that the event arrived without user OAuth context. System events cannot use user-token-dependent `app.info` resolution.

## SDK signals

The SDK can emit internal signals when an OAuth token is renewed or when a portal domain changes.

Install signal support first:

```bash
pip install "b24pysdk[signals]"
```

The main events are:

- `OAuthTokenRenewedEvent`
- `PortalDomainChangedEvent`

```python
from b24pysdk import BitrixToken
from b24pysdk.events import OAuthTokenRenewedEvent, PortalDomainChangedEvent


class MyBitrixToken(BitrixToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oauth_token_renewed_signal.connect(self.oauth_token_renewed_handler)
        self.portal_domain_changed_signal.connect(self.portal_domain_changed_handler)

    def oauth_token_renewed_handler(self, event: OAuthTokenRenewedEvent):
        print("Renewed OAuth token:", event.renewed_oauth_token)

    def portal_domain_changed_handler(self, event: PortalDomainChangedEvent):
        print("Domain changed:", event.old_domain, "->", event.new_domain)
```

Without the `signals` extra, regular SDK calls and token refresh continue to work. Direct imports from `b24pysdk.signals` raise an `ImportError` with an installation hint.

## Framework integrations

B24PySDK includes integrations for handling Bitrix24 placement launches, events, and workflow robot callbacks in common Python web frameworks.

The integrations collect incoming request parameters, parse them into the typed credential models described above, and optionally validate auth data against Bitrix24 `app.info`.

For incoming requests, JSON body data is collected first, query-string values override matching JSON keys, and form values override matching JSON/query keys. Repeated query/form values are preserved as lists.

### Django

Install:

```bash
pip install "b24pysdk[django]"
```

The Django integration provides:

- `@placement_required`
- `@event_required`
- `@workflow_required`
- `PlacementRequest`
- `EventRequest`
- `WorkflowRequest`

Example:

```python
from django.http import JsonResponse

from b24pysdk.integrations.django.decorators import placement_required
from b24pysdk.integrations.django.types import PlacementRequest


@placement_required
def placement_view(request: PlacementRequest):
    return JsonResponse({
        "domain": request.oauth_placement_data.domain,
    })
```

Pass `bitrix_app=bitrix_app` to a decorator when the incoming auth data must be validated against Bitrix24 `app.info`.

See `b24pysdk/integrations/django/README.md` for details.

### FastAPI

Install:

```bash
pip install "b24pysdk[fastapi]"
```

The FastAPI integration provides dependencies for placement, event, and workflow endpoints.

```python
from typing import Annotated

from fastapi import Depends, FastAPI

from b24pysdk.credentials import OAuthPlacementData
from b24pysdk.integrations.fastapi.dependencies import placement_dependency

app = FastAPI()


@app.post("/placement")
async def placement_handler(
    placement: Annotated[OAuthPlacementData, Depends(placement_dependency)],
):
    return {"domain": placement.domain}
```

For normal endpoints, use the ready-made `placement_dependency`, `event_dependency`, and `workflow_dependency`.

When auth data must also be validated through `app.info`, use `get_placement_dependency(bitrix_app=bitrix_app)` or the corresponding `get_event_dependency(...)` / `get_workflow_dependency(...)` factory.

See `b24pysdk/integrations/fastapi/README.md` for details.

### Flask

Install:

```bash
pip install "b24pysdk[flask]"
```

The Flask integration provides decorators and typed helper accessors.

```python
from flask import Flask

from b24pysdk.integrations.flask.decorators import placement_required
from b24pysdk.integrations.flask.dependencies import get_oauth_placement_data

app = Flask(__name__)


@app.post("/placement")
@placement_required
def placement_handler():
    return {
        "domain": get_oauth_placement_data().domain,
    }
```

Parsed data is stored in `flask.g`. Pass `bitrix_app=bitrix_app` to the integration decorators when `app.info` validation is required.

See `b24pysdk/integrations/flask/README.md` for details.

## Abstract credential classes

Applications that persist credentials in an ORM or another storage layer can build on the SDK abstract credential classes:

- `AbstractBitrixApp`
- `AbstractBitrixAppLocal`
- `AbstractBitrixToken`
- `AbstractBitrixTokenLocal`

Concrete applications are responsible for implementing and storing the required attributes while reusing the SDK authentication and request behavior.

## Package structure

The main package is organized around a small set of public SDK areas:

```text
b24pysdk/
├── api/               # request, response, pagination, batch, and transport layers
├── constants/         # Bitrix24 and SDK constants/enums
├── credentials/       # webhook, OAuth app/token, and callback payload models
├── errors/            # REST, transport, HTTP, and OAuth exceptions
├── events/            # SDK event payloads
├── integrations/      # Django, FastAPI, and Flask integrations
├── log/               # logger abstractions and implementations
├── objects/           # typed objects, field descriptors, managers, and object results
├── protocols/         # shared typing protocols
├── schemas/           # typed API/result schemas and adapters
├── scopes/            # Bitrix24 REST method wrappers
├── signals/           # optional signal implementation
├── utils/             # shared utilities and type aliases
├── _config.py         # runtime SDK configuration
├── _version.py        # package version metadata
└── client.py          # Client factory and versioned clients
```

For application development, the most commonly used public entry points are the top-level package exports, `credentials`, `constants`, `errors`, `schemas`, `scopes`, `objects`, `integrations`, and `log`. Internal implementation modules under these packages do not need to be imported directly unless explicitly documented.

## Supported REST areas

The high-level client currently exposes wrappers for a broad set of Bitrix24 REST areas.

Common client contexts include:

- `access`
- `ai`
- `app`
- `booking`
- `biconnector`
- `bizproc`
- `calendar`
- `catalog`
- `crm`
- `department`
- `disk`
- `documentgenerator`
- `entity`
- `event`
- `events`
- `feature`
- `im`
- `imbot`
- `imconnector`
- `imopenlines`
- `landing`
- `lists`
- `log`
- `mailservice`
- `messageservice`
- `method`
- `placement`
- `profile`
- `pull`
- `rpa`
- `sale`
- `salescenter`
- `scope`
- `server`
- `sign`
- `socialnetwork`
- `sonet_group`
- `task`
- `telephony`
- `user`
- `userconsent`
- `userfieldconfig`
- `userfieldtype`
- `vote`
- `voximplant`

The v2 client additionally exposes `tasks` and `timeman`.

The v3 client exposes v3-specific contexts including `call`, `documentation`, `humanresources`, `mail`, `main`, `note`, `rest`, `tasks`, and `timeman`.

Not every Bitrix24 REST method is necessarily wrapped yet. Use `get_supported_api_methods()` to inspect the exact supported surface for the selected client, and use low-level token calls for methods without a wrapper.

## SDK metadata

Stable SDK metadata is available from the top-level package:

```python
from b24pysdk import SDK_NAME, SDK_VERSION, __version__

print(SDK_NAME)
print(SDK_VERSION)
print(__version__)
```

`SDK_VERSION` and `__version__` represent the installed SDK version.

The installed version can also be printed from the command line:

```bash
python -m b24pysdk
```

## Development and tests

The project supports Python 3.9+.

Install development and test dependencies directly when needed:

```bash
pip install -e ".[dev,test]"
```

### Docker development

The repository contains Docker-based test and development environments.

Build the reusable development image:

```bash
make build-dev
```

Run Ruff against the mounted working tree:

```bash
make lint
```

Open a development shell:

```bash
make shell
```

### Test image

The current Makefile exposes dedicated targets that build the test image and run the requested test group:

```bash
make test-all
make test-integration
make test-integration-webhook
make test-integration-oauth
make test-unit
```

Run tests by marker:

```bash
make test-marker M=unit
```

Run a specific test path:

```bash
make test-path TEST_PATH=tests/integration/unit
```

Integration targets use `.env.local` in the current Makefile. Typical credentials are:

```text
B24_DOMAIN=example.bitrix24.com
B24_WEBHOOK=1/webhook_key
```

OAuth-based integration tests additionally require the corresponding OAuth application/token variables used by the test configuration.

### CI

GitHub Actions currently runs Ruff and unit tests on Python 3.9 and Python 3.14. A Docker CI job also runs unit tests and a webhook profile smoke test.

## License

B24PySDK is distributed under the MIT License. See `LICENSE` for details.
