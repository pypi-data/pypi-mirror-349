import json
from typing import Any

LITERAL_VALUE = "*LITERAL_VALUE"


def merge_dicts(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> dict[Any, Any]:
    """
    Merges two dictionaries recursively and reduces the duplicated keys to a list.
    """
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = merge_dicts(merged_dict[key], value)
        elif key in merged_dict:
            merged_dict[key] = (
                [merged_dict[key], value] if not isinstance(merged_dict[key], list) else merged_dict[key] + [value]
            )
        else:
            merged_dict[key] = value

    return merged_dict


def clean_dict(ast: Any) -> Any:
    output = delete_empty_data(ast)
    output = transform_literals(output)
    return parse_json_strings(output)


def parse_json_strings(data: Any) -> Any:
    """
    Recursively parse JSON strings in the data.
    """
    if isinstance(data, dict):
        return {k: parse_json_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_json_strings(el) for el in data]
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    return data


def delete_empty_data(data: Any) -> Any:
    """
    Recursivele delete null values, empty dictionaries and lists from the data.
    """
    if isinstance(data, dict):
        cleaned_dict = {k: delete_empty_data(v) for k, v in data.items()}
        return {k: v for k, v in cleaned_dict.items() if not (isinstance(v, (dict, list)) and len(v) == 0 or v is None)}
    elif isinstance(data, list):
        cleaned_list = [delete_empty_data(el) for el in data]
        return [el for el in cleaned_list if not (isinstance(el, (dict, list)) and len(el) == 0 or el is None)]

    return data


def transform_literals(data: Any) -> Any:
    """
    Transforms dictionaries where the key is LITERAL_VALUE to the value of the key.
    """
    if isinstance(data, dict):
        if LITERAL_VALUE in data and len(data) == 1:
            return data[LITERAL_VALUE]
        else:
            return {k: transform_literals(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_literals(el) for el in data]

    return data
