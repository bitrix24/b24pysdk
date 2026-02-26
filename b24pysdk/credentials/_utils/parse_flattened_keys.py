import re
from typing import Any, Mapping, Text

from ...utils.types import JSONDict

__all__ = [
    "parse_flattened_keys",
]


def _transform(data: Any) -> Any:
    """Recursively converts dictionaries with sequential numeric keys into lists"""

    if not isinstance(data, dict):
        return data

    transformed_data: JSONDict = {}

    for key, value in data.items():
        transformed_data[key] = _transform(value)

    if transformed_data and all(key.isdigit() for key in transformed_data):
        indices = sorted(int(key) for key in transformed_data)

        if indices == list(range(len(indices))):
            return [transformed_data[str(index)] for index in indices]

    return transformed_data


def parse_flattened_keys(data: Mapping[Text, Any]) -> JSONDict:
    """Parses flat dictionary keys with square bracket notation into a nested structure"""

    result_data: JSONDict = {}

    for raw_key, raw_value in data.items():

        value = (
            raw_value[0]
            if isinstance(raw_value, list) and len(raw_value) == 1
            else raw_value
        )

        parts = re.findall(r"[^\[\]]+", raw_key)
        current_level = result_data

        for part in parts[:-1]:
            current_level = current_level.setdefault(part, {})

        current_level[parts[-1]] = value

    return _transform(result_data)
