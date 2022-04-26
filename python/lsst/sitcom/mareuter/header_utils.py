__all__ = ["get_from_json"]

from typing import Any


def get_from_json(column: str, info: dict) -> Any:
    series = info["results"][0]["series"][0]
    index = series["columns"].index(column)
    result = series["values"][0][index]
    return result
