#!/usr/bin/env python
import argparse
import operator

from prettytable import PrettyTable, TableStyle

import lsst.daf.butler as dafButler

HEADER = ["ObsId", "SeqNum", "ObsType", "ExpTime", "DarkTime", "Filter", "Target"]


def main(opts: argparse.Namespace) -> None:
    if opts.embargo:
        repo = "/repo/embargo"
    else:
        repo = opts.instrument

    butler = dafButler.Butler(
        repo,
        collections=[f"{opts.instrument}/raw/all"],
        instrument=opts.instrument,
    )

    where_clause = [
        f"exposure.day_obs={opts.day_obs}",
        f"exposure.seq_num>={opts.seq_start}",
        f"exposure.seq_num<={opts.seq_end}",
    ]

    selection = " and ".join(where_clause)

    records = butler.registry.queryDimensionRecords("exposure", where=selection)
    records = sorted(records, key=operator.attrgetter("seq_num"))

    if not records:
        raise RuntimeError(f"No records found from selection: {selection}")

    if opts.show_first_record:
        print(list(records)[0])

    table = PrettyTable()
    table.align = "l"
    table.field_names = HEADER
    for record in records:
        table.add_row(
            [
                record.obs_id,
                record.seq_num,
                record.observation_type,
                record.exposure_time,
                record.dark_time,
                record.physical_filter,
                record.target_name,
            ]
        )

    table.align = "l"
    table.float_format["DarkTime"] = ".6"
    table.set_style(TableStyle.DOUBLE_BORDER)
    print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("instrument")
    parser.add_argument("day_obs")
    parser.add_argument("seq_start")
    parser.add_argument("seq_end")

    parser.add_argument("--show-first-record", action="store_true")
    parser.add_argument("-e", "--embargo", action="store_true")

    args = parser.parse_args()
    main(args)
