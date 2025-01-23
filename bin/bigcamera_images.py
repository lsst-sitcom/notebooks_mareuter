#!/usr/bin/env python
import argparse
import collections

from prettytable import PrettyTable, TableStyle

import lsst.daf.butler as dafButler

HEADER = ["Exposure", "Num Detectors"]


def main(opts: argparse.Namespace) -> None:
    instrument = "LSSTCam"

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

    records = butler.registry.queryDatasets("raw", where=selection)

    if not len(list(records)):
        raise RuntimeError(f"No records found from selection: {selection}")

    exposures = collections.defaultdict(list)

    for record in records:
        exposures[record.dataId["exposure"]].append(record.dataId["detector"])

    exposure_list = sorted(exposures.items())

    table = PrettyTable()
    table.field_names = HEADER

    for exposure in exposure_list:
        table.add_row([exposure[0], len(exposure[1])])

    table.align[HEADER[0]] = "l"
    table.align[HEADER[1]] = "c"
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
