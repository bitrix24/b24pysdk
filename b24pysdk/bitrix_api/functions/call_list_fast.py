from typing import Dict, Optional, Text

from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from .call_batches import call_batches

BATCH_SIZE = 50
HALT = True
DEFAULT_ID_FIELD = "ID"


def _deep_merge(*dicts: dict) -> dict:
    """
    Merges nested dictionaries recursively
    """
    res = {}
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict):
                if k in res and not isinstance(res[k], (dict, type(None))):
                    raise ValueError(f"cannot merge {v} into {res[k]}")
                res[k] = _deep_merge(res.get(k) or {}, v)
                continue
            res[k] = v
    return res


def _order_by_id(request_id_field: Text, descending: bool = False) -> dict:
    """
    Generate order by ID parameter
    """
    return {"order": {request_id_field: "DESC" if descending else "ASC"}}


def _filter_by_id(
        request_id_field: Text,
        response_id_field: Text,
        index: int,
        last_id: Optional[int] = None,
        wrapper: Optional[str] = None,
        descending: bool = False,
) -> dict:
    """
    Generate filter by id
    """

    cmp = "<" if descending else ">"
    prop = f"{cmp}{request_id_field}"
    if index == 0:
        if last_id is not None:
            return {"filter": {prop: last_id}}
        return {}
    path = f"$result[req_{index - 1}]"
    if wrapper:
        path = f"{path}[{wrapper}]"
    return {"filter": {prop: f"{path}[49][{response_id_field}]"}}


def _generate_batch_methods(
        api_method: Text,
        params: Optional[dict],
        request_id_field: Text,
        response_id_field: Text,
        descending: bool,
        wrapper: Optional[Text],
        last_item_id: Optional[int],
) -> Dict[Text, B24BatchRequestData]:
    """
    Generates list of methods, using call_list_fast() api_method and params, adding filter by ID

    Returns:
        dict of B24BatchRequestData, ready to be used by call_batches()
    """

    methods = {}
    for i in range(BATCH_SIZE):
        batch_params = _deep_merge(
            dict() if params is None else params,
            _order_by_id(request_id_field, descending),
            _filter_by_id(
                request_id_field=request_id_field,
                response_id_field=response_id_field,
                index=i,
                last_id=last_item_id,
                wrapper=wrapper,
                descending=descending,
            ),
            dict(start=-1),
        )
        methods[f"req_{i}"] = (api_method, batch_params)

    return methods


def call_list_fast(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        limit: Optional[int] = None,
        request_id_field: Text = DEFAULT_ID_FIELD,
        response_id_field: Text = DEFAULT_ID_FIELD,
        wrapper: Optional[Text] = None,
        descending: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONList:
    """
    Retrieve large number of items using filter by ID and start=-1 parameter to disable the count of items

    Args:
        domain: portal domain
        auth_token: auth token
        is_webhook: is webhook token
        api_method: api method to call
        params: doct of method parameters
        limit: max number of items to retrieve
        request_id_field: name of the item ID field to be passed in parameters
        response_id_field: name of the item ID field to be received in response
        wrapper: name of the property if items list is nested in the response
        descending: is order descending
        timeout: timeout in seconds

    Returns:
        list of items
    """

    items = []
    last_item_id = None
    while True:
        methods = _generate_batch_methods(
            api_method=api_method,
            params=params,
            request_id_field=request_id_field,
            response_id_field=response_id_field,
            descending=descending,
            wrapper=wrapper,
            last_item_id=last_item_id,
        )

        batch = call_batches(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            methods=methods,
            halt=HALT,
            timeout=timeout,
            **kwargs,
        )

        results: JSONDict = batch["result"]["result"]
        for batch_items in results.values():
            if wrapper:
                batch_items = batch_items[wrapper]

            items.extend(batch_items)

            if limit is not None and len(items) >= limit:
                return items[:limit]

            if len(batch_items) < BATCH_SIZE:
                return items

            last_item_id = items[-1][response_id_field]
