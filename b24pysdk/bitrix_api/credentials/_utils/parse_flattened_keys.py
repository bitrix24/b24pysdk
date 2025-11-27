import re
from typing import Any, List, Mapping, Text, Union

from ....utils.types import JSONDict


def _take_value(value: Any) -> Any:
    """"""
    if isinstance(value, list) and len(value) == 1:
        return value[0]
    return value


def parse_flattened_keys(input_mapping: Mapping[Text, Any]) -> JSONDict:
    """"""

    output_dict: JSONDict = dict()

    for raw_key, raw_value in input_mapping.items():
        value = _take_value(raw_value)

        parts = re.findall(r"[^\[\]]+", raw_key)
        current: Union[List, Mapping] = output_dict

        for index, part in enumerate(parts, 1):
            if index < len(parts):
                next_part = parts[index]

                if part not in current:
                    current[part] = list() if next_part.isdigit() else dict()

                current = current[part]

            elif part.isdigit():
                int_part = int(part)

                while len(current) <= int_part:
                    current.append(None)

                current[int_part] = value
            else:
                current[part] = value

    return output_dict
