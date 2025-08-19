from datetime import datetime
from typing import Dict, Generator, Iterable, List, Optional, Text, Union

from ..._constants import MAX_BATCH_SIZE
from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from .call_batch import call_batch

_DEFAULT_ID_FIELD = "ID"
_HALT = True


def _force_values(collection: Union[Dict, List]) -> Iterable[Union[JSONDict, JSONList]]:
    """"""
    if isinstance(collection, dict):
        return collection.values()
    else:
        return collection


def _deep_merge(*dicts: Dict) -> Dict:
    """
    Merges nested dictionaries recursively
    """

    result_dict: Dict = {}

    for current_dict in dicts:

        for key, value in current_dict.items():
            existing_value = result_dict.get(key)

            if isinstance(value, dict):

                if existing_value is not None and not isinstance(existing_value, dict):
                    raise ValueError(f"Cannot merge a dict into a non-dict at key '{key}': {existing_value}")

                result_dict[key] = _deep_merge(existing_value or {}, value)
            else:
                result_dict[key] = value

    return result_dict


def _order_by_id(request_id_field: Text, descending: bool = False) -> JSONDict:
    """
    Generate order by ID parameter
    """
    return {"order": {request_id_field: "DESC" if descending else "ASC"}}


def _filter_by_id(
        request_id_field: Text,
        response_id_field: Text,
        index: int,
        last_id: Optional[int],
        wrapper: Optional[Text],
        descending: bool,
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

    return {"filter": {prop: f"{path}[{MAX_BATCH_SIZE - 1}][{response_id_field}]"}}


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

    methods: Dict[Text, B24BatchRequestData] = dict()
    order_dict: JSONDict = _order_by_id(request_id_field, descending)

    for index in range(MAX_BATCH_SIZE):
        batch_params = _deep_merge(
            params,
            order_dict,
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


def _add_time(target_time: JSONDict, term_time: JSONDict):
    """"""

    target_time["finish"] = term_time["finish"]
    target_time["duration"] += term_time["duration"]
    target_time["processing"] += term_time["processing"]
    target_time["date_finish"] = term_time["date_finish"]

    if target_time.get("operating_reset_at") is not None:
        target_time["operating_reset_at"] = term_time["operating_reset_at"]

    if target_time.get("operating") is not None:
        target_time["operating"] = term_time["operating"]


def _generate_result(
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: JSONDict,
        limit: Optional[int],
        request_id_field: Text,
        response_id_field: Text,
        wrapper: Optional[Text],
        descending: bool,
        timeout: Timeout,
        time: JSONDict,
        **kwargs,
) -> Generator[JSONDict, None, None]:
    """"""

    counter = 0
    last_entity_id = None

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

        batch_response = call_batch(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            methods=methods,
            halt=_HALT,
            timeout=timeout,
            **kwargs,
        )

        _add_time(time, batch_response["time"])

        results: Union[JSONDict, JSONList] = batch_response["result"]["result"]

        if not results:
            return

        for result_values in _force_values(results):
            if wrapper:
                unwrapped_values = result_values[wrapper]
            else:
                unwrapped_values = result_values

            for result_value in unwrapped_values:
                yield result_value
                counter += 1

                if limit is not None and counter >= limit:
                    return

            if len(unwrapped_values) < MAX_BATCH_SIZE:
                return

            last_entity_id = unwrapped_values[-1][response_id_field]


def call_list_fast(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        limit: Optional[int] = None,
        request_id_field: Text = _DEFAULT_ID_FIELD,
        response_id_field: Text = _DEFAULT_ID_FIELD,
        wrapper: Optional[Text] = None,
        descending: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict:
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

    if params is None:
        params = dict()

    now_datetime = datetime.now().astimezone()

    time = dict(
        start=now_datetime.timestamp(),
        finish=now_datetime.timestamp(),
        duration=0,
        processing=0,
        date_start=now_datetime.isoformat(timespec="seconds"),
        date_finish=now_datetime.isoformat(timespec="seconds"),
    )

    return dict(
        result=_generate_result(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            limit=limit,
            request_id_field=request_id_field,
            response_id_field=response_id_field,
            wrapper=wrapper,
            descending=descending,
            timeout=timeout,
            time=time,
            **kwargs,
        ),
        time=time,
    )
