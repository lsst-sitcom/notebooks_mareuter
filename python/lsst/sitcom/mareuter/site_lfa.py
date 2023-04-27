from dataclasses import dataclass
import os


@dataclass
class LfaInfo:
    endpoint_url: str
    bucket: str
    profile: str


def get_lfa() -> LfaInfo:
    """Get the LFA information from the LSST_DDS_PARTITION_PREFIX envvar

    Returns
    -------
    `LfaInfo`
        The information for the site LFA

    Raises
    ------
    RuntimeError
        If the value of LSST_DDS_PARTITION_PREFIX is not recognized
    """
    try:
        label = os.environ["LSST_DDS_PARTITION_PREFIX"]
        lfa = None
        if label == "tucson":
            lfa = LfaInfo("https://s3.tu.lsst.org", "rubinobs-lfa-tuc", "tts")
        if label == "base":
            lfa = LfaInfo("https://s3.ls.lsst.org", "rubinobs-lfa-ls", "bts")
        if label == "summit":
            lfa = LfaInfo("https://s3.cp.lsst.org", "rubinobs-lfa-cp", "summit")
        if lfa is not None:
            return lfa
        raise RuntimeError(f"Cannot provide EFD name for {label}.")
    except KeyError:
        raise RuntimeError("LSST_DDS_PARTITION_PREFIX not defined")
