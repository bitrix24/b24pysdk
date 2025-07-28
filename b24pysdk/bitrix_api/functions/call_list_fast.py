from typing import Dict, Optional, Text

from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from .call_batches import call_batches

BATCH_SIZE = 50
HALT = True
DEFAULT_ID_FIELD = "ID"


def _deep_merge(*dicts: Dict) -> Dict:
    """
    Merges nested dictionaries recursively
    """

    result: Dict = {}

    for current_dict in dicts:

        for key, value in current_dict.items():
            existing_value = result.get(key)

            if isinstance(value, dict):

                if existing_value is not None and not isinstance(existing_value, dict):
                    raise ValueError(f"Cannot merge a dict into a non-dict at key '{key}': {existing_value}")

                result[key] = _deep_merge(existing_value or {}, value)
            else:
                result[key] = value

    return result


def _order_by_id(request_id_field: Text, descending: bool = False) -> Dict:
    """
    Generate order by ID parameter
    """
    return {"order": {request_id_field: "DESC" if descending else "ASC"}}


def _filter_by_id(
        request_id_field: Text,
        response_id_field: Text,
        index: int,
        last_id: Optional[int] = None,
        wrapper: Optional[Text] = None,
        descending: bool = False,
) -> Dict:
    """
    Generate filter by id
    """

    cmp = "<" if descending else ">"
    prop = f"{cmp}{request_id_field}"

    if index == 0:
        if last_id is not None:
            return {"filter": {prop: last_id}}
        else:
            return {}

    path = f"$result[req_{index - 1}]"

    if wrapper:
        path = f"{path}[{wrapper}]"

    return {"filter": {prop: f"{path}[{BATCH_SIZE - 1}][{response_id_field}]"}}


def _generate_batch_methods(
        api_method: Text,
        params: Dict,
        request_id_field: Text,
        response_id_field: Text,
        descending: bool,
        wrapper: Optional[Text],
        last_entity_id: Optional[int],
) -> Dict[Text, B24BatchRequestData]:
    """
    Generates list of methods, using call_list_fast() api_method and params, adding filter by ID

    Returns:
        dict of B24BatchRequestData, ready to be used by call_batches()
    """

    methods: Dict[Text, B24BatchRequestData] = {}

    for index in range(BATCH_SIZE):
        batch_params = _deep_merge(
            params,
            _order_by_id(request_id_field, descending),
            _filter_by_id(
                request_id_field=request_id_field,
                response_id_field=response_id_field,
                index=index,
                last_id=last_entity_id,
                wrapper=wrapper,
                descending=descending,
            ),
            dict(start=-1),
        )
        methods[f"req_{index}"] = (api_method, batch_params)

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

    entities = []
    last_entity_id = None

    if params is None:
        params = dict()

    while True:
        methods = _generate_batch_methods(
            api_method=api_method,
            params=params,
            request_id_field=request_id_field,
            response_id_field=response_id_field,
            descending=descending,
            wrapper=wrapper,
            last_entity_id=last_entity_id,
        )

        batch_response = call_batches(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            methods=methods,
            halt=HALT,
            timeout=timeout,
            **kwargs,
        )

        results: JSONDict = batch_response["result"]["result"]

        for batch_items in results.values():
            if wrapper:
                batch_items = batch_items[wrapper]

            entities.extend(batch_items)

            if limit is not None and len(entities) >= limit:
                return entities[:limit]

            if len(batch_items) < BATCH_SIZE:
                return entities

            last_entity_id = entities[-1][response_id_field]
