import pathlib

__all__ = ["get_data_dir", "get_mplstyle_file"]


def get_data_dir() -> pathlib.Path:
    """Return the data directory of this package."""
    return pathlib.Path(__file__).resolve().parent / "data"


def get_mplstyle_file() -> pathlib.Path:
    """Return the matplotlib style file."""
    return get_data_dir() / "plot_style.mplstyle"
