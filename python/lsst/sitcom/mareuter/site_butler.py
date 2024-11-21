from dataclasses import dataclass
import os


@dataclass
class ButlerInfo:
    endpoint_url: str
    bucket: str
    profile: str


def get_butler(butler_type: str) -> ButlerInfo:
    """Get the Butler information from the LSST_SITE envvar

    Returns
    -------
    `ButlerInfo`
        The information for the site Butler

    Raises
    ------
    RuntimeError
        If the value of LSST_SITE is not recognized
    """
    try:
        label = os.environ["LSST_SITE"]
        endpoint_url = None
        if label == "tucson":
            endpoint_url = "https://s3-butler.tu.lsst.org"
        if label == "base":
            endpoint_url = "https://s3-butler.ls.lsst.org"
        if label == "summit":
            endpoint_url = "https://s3-butler.cp.lsst.org"
        if endpoint_url is not None:
            return ButlerInfo(endpoint_url, f"rubinobs-{butler_type}", "butler")
        raise RuntimeError(f"Cannot provide Butler info for {label}.")
    except KeyError:
        raise RuntimeError("LSST_SITE not defined")
