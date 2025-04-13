import os


def get_efd() -> str:
    """Get the EFD name from the LSST_SITE envvar

    Returns
    -------
    str
        The name of the EFD

    Raises
    ------
    RuntimeError
        If the value of LSST_SITE is not recognized
    """
    try:
        label = os.environ["LSST_SITE"]
        if label == "summit":
            return "summit_efd"
        if label == "tucson":
            return "tucson_teststand_efd"
        if label == "base":
            return "base_efd"
        raise RuntimeError(f"Cannot provide EFD name for {label}.")
    except KeyError:
        return "usdf_efd"
