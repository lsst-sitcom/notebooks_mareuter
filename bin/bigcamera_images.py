#!/usr/bin/env python
import argparse
import collections
import operator

from prettytable import PrettyTable, TableStyle
import requests

import lsst.daf.butler as dafButler
from lsst.sitcom.mareuter.process_helpers import run_cmd
from lsst.sitcom.mareuter.site_butler import get_butler
from lsst.sitcom.mareuter.site_lfa import get_lfa

HEADER = ["Exposure", "Num Detectors", "Expected Num Detectors", "Missing Detectors"]


def main(opts: argparse.Namespace) -> None:
    instrument = "LSSTCam"
    lfa_info = get_lfa()
    raw_info = get_butler("raw-lsstcam")

    if opts.embargo:
        repo = "/repo/embargo"
    else:
        repo = instrument

    butler = dafButler.Butler(
        repo,
        collections=[f"{instrument}/raw/all"],
        instrument=instrument,
    )

    where_clause = [
        f"exposure.day_obs={opts.day_obs}",
        f"exposure.seq_num>={opts.seq_start}",
        f"exposure.seq_num<={opts.seq_end}",
    ]

    selection = " and ".join(where_clause)

    dim_records = butler.registry.queryDimensionRecords("exposure", where=selection)
    dim_records = sorted(dim_records, key=operator.attrgetter("seq_num"))

    if not dim_records:
        raise RuntimeError(f"No dimension records found from selection: {selection}")

    data_records = butler.registry.queryDatasets("raw", where=selection)

    if not len(list(data_records)):
        raise RuntimeError(f"No dataset records found from selection: {selection}")

    exposures = collections.defaultdict(list)

    for data_record in data_records:
        exposures[data_record.dataId["exposure"]].append(data_record.dataId["detector"])

    base_url = f"{lfa_info.endpoint_url}/{lfa_info.bucket}/MTCamera/{opts.day_obs}/"

    detector_lists = {}
    for dim_record in dim_records:
        fetch_url = f"{base_url}/{dim_record.obs_id}_expectedSensors.json"
        result = requests.get(fetch_url)
        det_info = result.json()["expectedSensors"]
        detector_lists[dim_record.obs_id] = {
            "sensors": list(det_info.keys()),
            "images": [],
            "diff": None,
            "exposure": dim_record.exposure,
        }

        cmd = [
            "aws",
            "--profile",
            f"{raw_info.profile}",
            f"--endpoint-url={raw_info.endpoint_url}",
            "s3",
            "ls",
            f"{raw_info.bucket}/LSSTCam/{opts.day_obs}/{dim_record.obs_id}/",
        ]

        files_listing = run_cmd(cmd, as_lines=True)
        for file_listing in files_listing[:-1]:
            rfile = files_listing.strip().split()[-1]
            if rfile.endswith("fits"):
                detector_lists[dim_record.obs_id]["images"].append(rfile)

    for key, item in detector_lists.items():
        image_sensors = []
        for ifile in item["images"]:
            file_stem = ifile.split(".")[0]
            sensor = "_".join(file_stem.split("_")[-2:])
            image_sensors.append(sensor)

        detector_lists[key]["diff"] = set(item["sensors"]).difference(
            set(image_sensors)
        )

    table = PrettyTable()
    table.field_names = HEADER

    for obs_id, values in detector_lists.items():
        table.add_row(
            [
                obs_id,
                len(exposures[values["exposure"]]),
                len(values["sensors"]),
                ",".join(values["diff"]),
            ]
        )

    table.align[HEADER[0]] = "l"
    table.align[HEADER[1]] = "c"
    table.align[HEADER[2]] = "c"
    table.align[HEADER[3]] = "c"
    table.set_style(TableStyle.DOUBLE_BORDER)
    print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("day_obs")
    parser.add_argument("seq_start")
    parser.add_argument("seq_end")

    parser.add_argument("-e", "--embargo", action="store_true")

    args = parser.parse_args()
    main(args)
