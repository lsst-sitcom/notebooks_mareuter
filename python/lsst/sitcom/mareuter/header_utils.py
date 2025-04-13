__all__ = ["dict_from_additional", "get_from_json", "get_value"]

import re
from typing import Any

import pandas as pd


def dict_from_additional(data: pd.DataFrame) -> dict:
    additional_keys = data["additionalKeys"].iloc[0].split(":")
    additional_values = re.split(r"(?<!\\):", data["additionalValues"].iloc[0])
    output = {}
    for key, value in zip(additional_keys, additional_values):
        if key == "groupId":
            output[key] = value.replace("\\", "")
        else:
            output[key] = value
    return output


def get_from_json(column: str, info: dict) -> Any:
    series = info["results"][0]["series"][0]
    index = series["columns"].index(column)
    result = series["values"][0][index]
    return result


def get_value(result: pd.DataFrame, column: str, index: int = 0) -> Any:
    try:
        value = result[column].iloc[index]
        return value
    except KeyError:
        print(f"{column} not found in dataframe!")
        return None
