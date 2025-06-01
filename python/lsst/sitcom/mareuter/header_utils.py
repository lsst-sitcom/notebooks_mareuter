__all__ = ["dict_from_additional", "get_from_json", "get_monitor_value", "get_value"]

import re
from typing import Any

import numpy as np
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


def get_monitor_value(
    last_data: pd.DataFrame, range_data: pd.DataFrame, column: str, operation: str
) -> Any:
    try:
        range_values = range_data[column].to_numpy()
    except KeyError:
        range_values = np.array([])

    try:
        last_value = last_data[column].to_numpy()
    except KeyError:
        print(f"{column} not found in dataframe!")
        return None

    values = np.hstack((last_value, range_values))
    op = getattr(np, operation)
    return op(values)


def get_value(result: pd.DataFrame, column: str, index: int = 0) -> Any:
    try:
        value = result[column].iloc[index]
        return value
    except KeyError:
        print(f"{column} not found in dataframe!")
        return None
