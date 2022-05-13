import asyncio
import copy
import pathlib

import fastparquet
import numpy as np
import pandas as pd

__all__ = [
    "find_fingerprint",
    "make_auxtel_image_dataframe",
    "make_comcam_image_dataframe",
]


async def calculate_statistics(dataId: dict, butler):
    raw = butler.get("raw", dataId)
    amps = raw.getDetector()
    amp_medians = [
        np.median(raw[amps[i].getRawDataBBox()].image.array) for i in range(len(amps))
    ]
    try:
        amp_medians.insert(0, dataId["detector.id"])
    except KeyError:
        amp_medians.insert(0, dataId["detector"])
    return amp_medians


async def find_fingerprint(
    day_obs: int,
    start_seq_num: int,
    end_seq_num: int,
    camera: str,
    butler,
) -> None:
    for seq_num in range(start_seq_num, end_seq_num + 1):
        medians = await globals()[f"make_{camera}_image_dataframe"](
            day_obs, seq_num, butler
        )
        input_dir = pathlib.Path(f"~/DATA/fingerprint/{camera}").expanduser()
        fingerprint_file = None
        for input_file in input_dir.glob("*.parq"):
            pf = fastparquet.ParquetFile(str(input_file))
            image_medians = pf.to_pandas()
            if medians.equals(image_medians):
                fingerprint_file = input_file
                break
        if fingerprint_file is not None:
            print(f"Image {seq_num} is {fingerprint_file}")
        else:
            print(f"Image {seq_num} not found.")


async def make_auxtel_image_dataframe(day_obs: int, seq_num: int, butler):
    dataId = {
        "instrument": "LATISS",
        "detector": 0,
        "exposure.day_obs": day_obs,
        "exposure.seq_num": seq_num,
    }
    ccd_medians = await asyncio.gather(*[calculate_statistics(dataId, butler)])
    return make_dataframe(ccd_medians)


async def make_comcam_image_dataframe(day_obs: int, seq_num: int, butler):
    dataId_temp = {
        "instrument": "LSSTComCam",
        "detector.raft": "R22",
        "detector.id": None,
        "exposure.day_obs": day_obs,
        "exposure.seq_num": seq_num,
    }
    dataIds = []
    for i in range(9):
        di = copy.deepcopy(dataId_temp)
        di["detector.id"] = i
        dataIds.append(di)
    ccd_medians = await asyncio.gather(
        *[calculate_statistics(dataId, butler) for dataId in dataIds]
    )
    return make_dataframe(ccd_medians)


def make_dataframe(data: list):
    columns = [f"Amp{i:02}" for i in range(16)]
    columns.insert(0, "DetId")
    return pd.DataFrame(data, columns=columns, dtype="float64")
