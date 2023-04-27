from dataclasses import dataclass
from operator import attrgetter

BYTE_CONV: int = 1024
SIZE_SUFFIXES: list[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]


@dataclass
class AwsDuInfo:
    key: str
    size_bytes: int
    num_objects: int


def get_human_size(byte_value: int) -> str:
    """Convert the number of bytes into a human readable form.

    Parameters
    ----------
    byte_value : `int`
        The number of bytes to format.

    Returns
    -------
    `str`
        The human readable form for the number of bytes.
    """
    human_size: str | None = None
    suffix: int | None = None
    dval: float | None = None
    for i in range(len(SIZE_SUFFIXES)):
        if byte_value == 0:
            dval = byte_value
            suffix = 0
            break
        dval = byte_value / (BYTE_CONV**i)
        if dval < 1.0:  # type: ignore
            dval = byte_value / (BYTE_CONV ** (i - 1))
            suffix = i - 1
            break
        suffix = i
    if suffix == 0:
        dval_str = f"{dval:.0f}"
    else:
        dval_str = f"{dval:.3f}"

    human_size = f"{dval_str} {SIZE_SUFFIXES[suffix]}"  # type: ignore
    return human_size


def sort_by_num_objects(keys: list[AwsDuInfo]) -> list[AwsDuInfo]:
    """Sort information by number of objects with largest first.

    Parameters
    ----------
    keys: `list`
        The list of LfaInfo objects to sort.

    Returns
    -------
    `list`
        The list of LfaInfo objects sorted by number of objects.
    """
    return sorted(keys, key=attrgetter("num_objects"), reverse=True)


def sort_by_size_bytes(keys: list[AwsDuInfo]) -> list[AwsDuInfo]:
    """Sort information by size of bytes with largest first.

    Parameters
    ----------
    keys: `list`
        The list of LfaInfo objects to sort.

    Returns
    -------
    `list`
        The list of LfaInfo objects sorted by size of bytes.
    """
    return sorted(keys, key=attrgetter("size_bytes"), reverse=True)


def sum_attribute(keys: list[AwsDuInfo], attr: str) -> int:
    """Get the sum of a given LfaInfo attribute.

    Parameters
    ----------
    keys : `list`
        The list of LfaInfo objects to sum.
    attr : `str`
        The attribute to sum.

    Returns
    -------
    `int`
        The sum of the given attribute.
    """
    return sum(getattr(x, attr) for x in keys)
