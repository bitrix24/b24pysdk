from typing import Text, Dict
import urllib.parse

from ...utils.types import B24BatchRequestData, RawStringParam


def convert_params(form_data):
    """
    Recursively converts list/tuple/dict to string that can be understood by Bitrix API

    Examples:

        >>> convert_params({"field": {"hello": "world"}})
        "field[hello]=world"

        >>> convert_params([{"field": "hello"}, {"field": "world"}])
        "0[field]=hello&1[field]=world"

        >>> convert_params({"auth": 123, "field": {"hello": "world"}})
        "auth=123&field[hello]=world"

        >>> convert_params({"FILTER": {">=PRICE": 15}})
        "FILTER[%3E%3DPRICE]=15"

        >>> convert_params({"FIELDS": {"POST_TITLE": "[1] + 1 == 11 // true"}})
        "FIELDS[POST_TITLE]=%5B1%5D%20%2B%201%20%3D%3D%2011%20//%20true"
    """

    def recursive_traverse(values, key=None):
        """
        Args:
            values: If argument is a string, returns a string of format "key=values", else returns a string of key-value pairs separated by "&" like so: "key=value&key=value"
            key: Equals to None during top-level call, and recursive calls pass inner keys like so: "" => "field" => "field[hello]" => "field[hello][there]" => ...
        """

        params = []

        if not isinstance(values, (dict, list, tuple)):
            # scalar values
            values = "" if values is None else values

            if isinstance(values, RawStringParam):
                values = str(values)
            else:
                # convert int, float, lazy_str to str
                values = urllib.parse.quote(_force_str(values))

            return f"{key!s}={values!s}"

        if key is not None and not values:
            # Some methods require to pass skipped params as empty arrays
            # For example https://apidocs.bitrix24.com/api-reference/tasks/deprecated/task-item/task-item-list
            #     "However, if some parameters need to be skipped, they still need to be passed, but as empty arrays: ORDER[]=&FILTER[]=&PARAMS[]=&SELECT[]="
            return f"{key!s}[]="

        # create key-value iterator from dict/list/tuple
        # indices are used as keys in case of lists and tuples
        iterable = values.items() if isinstance(values, dict) else enumerate(values)

        # recursively converts inner keys
        for inner_key, v in iterable:
            # only inner key is converted, because outer key can contain square brackets which need to be preserved
            inner_key = urllib.parse.quote(_force_str(inner_key))

            if key is not None:
                inner_key = f"{key!s}[{inner_key!s}]"

            result = recursive_traverse(v, inner_key)
            params.append(
                "&".join(result) if isinstance(result, list) else result
            )

        return params

    return "&".join(recursive_traverse(form_data))


def _force_str(s):
    """"""
    if issubclass(type(s), str):
        return s

    return str(s, encoding="utf-8", errors="strict") if isinstance(s, bytes) else str(s)


def encode_methods(methods: Dict[Text, B24BatchRequestData]) -> Dict[Text, RawStringParam]:
    """
    Urlencodes api methods and their params
    """
    def convert_method(method: B24BatchRequestData) -> RawStringParam:
        """
        Urlencodes api method and params
        """
        api_method, params = method
        params = {} if params is None else params
        return RawStringParam(f"{api_method}?{urllib.parse.quote(convert_params(params), safe='[]=')}")

    return {identifier: convert_method(method) for identifier, method in methods.items()}
