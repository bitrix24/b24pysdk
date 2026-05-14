# Django integration

Install with the Django extra:

```bash
pip install "b24pysdk[django]"
```

The integration provides decorators for Django views that receive Bitrix24
placement launches, event callbacks, and workflow robot callbacks.

## Placement

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

Pass `bitrix_app` when the incoming payload must be validated against
Bitrix24 `app.info`:

```python
@placement_required(bitrix_app=bitrix_app)
def placement_view(request: PlacementRequest):
    return JsonResponse({
        "domain": request.oauth_placement_data.domain,
    })
```

## Events

```python
from b24pysdk.integrations.django.decorators import event_required
from b24pysdk.integrations.django.types import EventRequest


@event_required
def event_view(request: EventRequest):
    return JsonResponse({
        "event": request.oauth_event_data.event,
    })
```

Use `@event_required(bitrix_app=bitrix_app)` to validate the event auth data
against `app.info`.

## Workflow robots

```python
from b24pysdk.integrations.django.decorators import workflow_required
from b24pysdk.integrations.django.types import WorkflowRequest


@workflow_required
def workflow_view(request: WorkflowRequest):
    return JsonResponse({
        "workflow_id": request.oauth_workflow_data.workflow_id,
    })
```

Use `@workflow_required(bitrix_app=bitrix_app)` to validate the workflow auth
data against `app.info`.

## Request data

Each decorator receives a regular Django `HttpRequest`, collects request
parameters into `request.params`, attaches the parsed Bitrix24 payload, and
then passes the enriched request object to the view.

For typing, annotate the view argument with the matching integration request
type:

```python
from b24pysdk.integrations.django.types import (
    EventRequest,
    PlacementRequest,
    WorkflowRequest,
)


@placement_required
def placement_view(request: PlacementRequest):
    params = request.params
    placement = request.oauth_placement_data
    return JsonResponse({"domain": placement.domain})


@event_required
def event_view(request: EventRequest):
    params = request.params
    event = request.oauth_event_data
    return JsonResponse({"event": event.event})


@workflow_required
def workflow_view(request: WorkflowRequest):
    params = request.params
    workflow = request.oauth_workflow_data
    return JsonResponse({"workflow_id": workflow.workflow_id})
```

The runtime transformation is:

- `HttpRequest` -> `PlacementRequest` with `request.params` and `request.oauth_placement_data`
- `HttpRequest` -> `EventRequest` with `request.params` and `request.oauth_event_data`
- `HttpRequest` -> `WorkflowRequest` with `request.params` and `request.oauth_workflow_data`

Validation errors return `401 Unauthorized`. Unexpected errors return
`500 Internal Server Error`.
