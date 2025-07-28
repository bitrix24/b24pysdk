import urllib.parse
from typing import Any, Iterable, List, Mapping, Optional, Text, Union

from .types import JSONDict, JSONList


def _force_str(value: Any) -> Text:
    """"""

    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return str(value, encoding="utf-8", errors="strict")
    else:
        return str(value)


def encode_params(params: Optional[Union[JSONDict, JSONList]]) -> Text:
    """
    Recursively converts list/tuple/dict to string that can be understood by Bitrix API

    Examples:

        >>> encode_params({"field": {"hello": "world"}})
        "field[hello]=world"

        >>> encode_params([{"field": "hello"}, {"field": "world"}])
        "0[field]=hello&1[field]=world"

        >>> encode_params({"auth": 123, "field": {"hello": "world"}})
        "auth=123&field[hello]=world"

        >>> encode_params({"FILTER": {">=PRICE": 15}})
        "FILTER[%3E%3DPRICE]=15"

        >>> encode_params({"FIELDS": {"POST_TITLE": "[1] + 1 == 11 // true"}})
        "FIELDS[POST_TITLE]=%5B1%5D+%2B+1+%3D%3D+11+%2F%2F+true"
    """

    if params is None:
        params = dict()

    def _traverse(values: Any, outer_key: Optional[Text] = None) -> List[Text]:
        """
        Args:
            values: If argument is a string, returns a string of format "key=values", else returns a string of key-value pairs separated by "&" like so: "key=value&key=value"
            outer_key: Equals to None during top-level call, and recursive calls pass inner keys like so: "" => "field" => "field[hello]" => "field[hello][there]" => ...
        """

        encoded_params: List[Text] = []

        if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
            # scalar values
            encoded_values = "" if values is None else urllib.parse.quote_plus(_force_str(values))

            return [f"{outer_key}={encoded_values}"]

        if outer_key is not None and not values:
            # Some methods require to pass skipped params as empty arrays
            # For example https://apidocs.bitrix24.com/api-reference/tasks/deprecated/task-item/task-item-list
            #     "However, if some parameters need to be skipped, they still need to be passed, but as empty arrays: ORDER[]=&FILTER[]=&PARAMS[]=&SELECT[]="
            return [f"{outer_key}[]="]

        # create key-value iterator from iterable
        items = values.items() if isinstance(values, Mapping) else enumerate(values)

        # recursively converts inner keys
        for inner_key, value in items:
            # only inner key is converted, because outer key can contain square brackets which need to be preserved
            inner_key = urllib.parse.quote_plus(_force_str(inner_key))

            if outer_key is not None:
                full_key = f"{outer_key}[{inner_key}]"
            else:
                full_key = inner_key

            encoded_params.extend(_traverse(value, full_key))

        return encoded_params

    return "&".join(_traverse(params))
