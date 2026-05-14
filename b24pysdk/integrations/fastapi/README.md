# FastAPI integration

Install with the FastAPI extra:

```bash
pip install "b24pysdk[fastapi]"
```

The integration provides FastAPI dependencies for Bitrix24 placement launches,
event callbacks, and workflow robot callbacks.

## Placement

```python
from typing import Annotated

from fastapi import Depends, FastAPI

from b24pysdk.credentials import OAuthPlacementData
from b24pysdk.integrations.fastapi.dependencies import get_placement_dependency

app = FastAPI()


@app.post("/placement")
async def placement_handler(
    placement: Annotated[OAuthPlacementData, Depends(get_placement_dependency())],
):
    return {
        "domain": placement.domain,
    }
```

Pass `bitrix_app` when the incoming payload must be validated against
Bitrix24 `app.info`:

```python
@app.post("/placement")
async def placement_handler(
    placement: Annotated[
        OAuthPlacementData,
        Depends(get_placement_dependency(bitrix_app=bitrix_app)),
    ],
):
    return {
        "domain": placement.domain,
    }
```

## Events

```python
from b24pysdk.credentials import OAuthEventData
from b24pysdk.integrations.fastapi.dependencies import get_event_dependency


@app.post("/event")
async def event_handler(
    event: Annotated[OAuthEventData, Depends(get_event_dependency())],
):
    return {
        "event": event.event,
    }
```

Use `Depends(get_event_dependency(bitrix_app=bitrix_app))` to validate the
event auth data against `app.info`.

## Workflow robots

```python
from b24pysdk.credentials import OAuthWorkflowData
from b24pysdk.integrations.fastapi.dependencies import get_workflow_dependency


@app.post("/workflow")
async def workflow_handler(
    workflow: Annotated[OAuthWorkflowData, Depends(get_workflow_dependency())],
):
    return {
        "workflow_id": workflow.workflow_id,
    }
```

Use `Depends(get_workflow_dependency(bitrix_app=bitrix_app))` to validate the
workflow auth data against `app.info`.

Validation errors raise `401 Unauthorized`. Unexpected errors raise
`500 Internal Server Error`.
