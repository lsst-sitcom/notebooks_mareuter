__all__ = ["check_float", "check", "check_near", "check_not_empty"]

from typing import Any

import numpy as np


def has_key(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            print(f"{args[0]} does not exist!")

    return wrapper


@has_key
def check(keyword: str, values: dict, truth: Any) -> None:
    value = values[keyword]
    if truth == value:
        print(f"{keyword} OK")
    else:
        print(f"Problem with {keyword}: {truth} != {value}")


@has_key
def check_float(
    keyword: str, values: dict, truth: float, precision: float = 1e-8
) -> None:
    value = values[keyword]
    try:
        diff = np.fabs(truth - value)
        if diff < precision:
            print(f"{keyword} OK")
        else:
            print(f"Problem with {keyword}: {truth} != {value}")
    except TypeError:
        print(f"Problem with {keyword}: {truth} != {value}                      ")


def check_near(
    keyword1: str, keyword2: str, values: dict, precision: float = 1.0
) -> None:
    value1 = values[keyword1]
    value2 = values[keyword2]
    diff = np.fabs(value1 - value2)
    if diff < precision:
        print(f"{keyword1} near {keyword2}")
    else:
        print(f"{keyword1} NOT near {keyword2}: {value1}, {value2}")


@has_key
def check_not_empty(keyword: str, values: dict) -> None:
    value = values[keyword]
    if value == "" or value is None:
        print(f"{keyword} is empty")
    else:
        print(f"{keyword} OK")
