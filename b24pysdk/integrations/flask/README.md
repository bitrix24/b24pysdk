# Flask integration

Install with the Flask extra:

```bash
pip install "b24pysdk[flask]"
```

The integration provides decorators for Flask handlers that receive Bitrix24
placement launches, event callbacks, and workflow robot callbacks.

Parsed data is stored in `flask.g`. Use helper functions from
`b24pysdk.integrations.flask.dependencies` when you want typed accessors.

## Placement

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

Pass `bitrix_app` when the incoming payload must be validated against
Bitrix24 `app.info`:

```python
@app.post("/placement")
@placement_required(bitrix_app=bitrix_app)
def placement_handler():
    return {
        "domain": get_oauth_placement_data().domain,
    }
```

## Events

```python
from b24pysdk.integrations.flask.decorators import event_required
from b24pysdk.integrations.flask.dependencies import get_oauth_event_data


@app.post("/event")
@event_required
def event_handler():
    return {
        "event": get_oauth_event_data().event,
    }
```

Use `@event_required(bitrix_app=bitrix_app)` to validate the event auth data
against `app.info`.

## Workflow robots

```python
from b24pysdk.integrations.flask.decorators import workflow_required
from b24pysdk.integrations.flask.dependencies import get_oauth_workflow_data


@app.post("/workflow")
@workflow_required
def workflow_handler():
    return {
        "workflow_id": get_oauth_workflow_data().workflow_id,
    }
```

Use `@workflow_required(bitrix_app=bitrix_app)` to validate the workflow auth
data against `app.info`.

## Request data

Each decorator collects request parameters into `g.params` and attaches the
parsed Bitrix24 payload:

- `g.oauth_placement_data`
- `g.oauth_event_data`
- `g.oauth_workflow_data`

Validation errors return `401 Unauthorized`. Unexpected errors return
`500 Internal Server Error`.
