#!/usr/bin/env python
import argparse

from prettytable import PrettyTable, TableStyle

import lsst.sitcom.mareuter.aws_du_helpers as adh
from lsst.sitcom.mareuter.process_helpers import run_cmd
from lsst.sitcom.mareuter.site_butler import get_butler
from lsst.sitcom.mareuter.site_lfa import get_lfa

SIZE_BYTES_HEADER = ["Key", "Bytes Size"]
NUM_OBJECTS_HEADER = ["Key", "Number of Objects"]


def main(opts: argparse.Namespace) -> None:
    if opts.butler is not None:
        info = get_butler(opts.butler)
    else:
        info = get_lfa()

    # Get all of the keys from the S3 bucket
    cmd = [
        "aws",
        "--profile",
        f"{info.profile}",
        f"--endpoint-url={info.endpoint_url}",
        "s3",
        "ls",
        f"{info.bucket}/",
    ]
    if opts.dir is not None:
        cmd[-1] += opts.dir
        insertion = opts.dir
    else:
        insertion = ""

    key_lines = run_cmd(cmd, as_lines=True)
    keys: list[str] = []
    for key_line in key_lines[:-1]:
        if opts.verbose:
            print("A:", key_line)
        parts = key_line.strip().split()
        keys.append(parts[-1])

    if opts.verbose:
        print(keys)

    print(f"Found {len(keys)} keys")

    cmd.extend(["--summarize", "--recursive"])

    du_info = []
    for key in keys:
        cmd[6] = f"{info.bucket}/{insertion}{key}"
        output = run_cmd(cmd, as_lines=True)
        name = key.strip("/")
        num_objects = int(output[-3].strip().split()[-1])
        size_bytes = int(output[-2].strip().split()[-1])
        du_info.append(adh.AwsDuInfo(name, size_bytes, num_objects))
        print(".", end="", flush=True)
    print()
    print()

    sorted_num_objects = adh.sort_by_num_objects(du_info)
    sorted_size_bytes = adh.sort_by_size_bytes(du_info)

    print("Keys Sorted by Size")
    table_size_bytes = PrettyTable()
    table_size_bytes.align = "l"
    table_size_bytes.field_names = SIZE_BYTES_HEADER
    for record in sorted_size_bytes:
        table_size_bytes.add_row([record.key, adh.get_human_size(record.size_bytes)])
    table_size_bytes.align = "l"
    table_size_bytes.set_style(TableStyle.DOUBLE_BORDER)
    print(table_size_bytes)
    print(
        f"Total Size Bytes: {adh.get_human_size(adh.sum_attribute(sorted_size_bytes, 'size_bytes'))}"
    )
    print()

    print("Keys Sorted by Number of Objects")
    table_num_objects = PrettyTable()
    table_num_objects.align = "l"
    table_num_objects.field_names = NUM_OBJECTS_HEADER
    for record in sorted_num_objects:
        table_num_objects.add_row([record.key, record.num_objects])
    table_num_objects.align = "l"
    table_num_objects.set_style(TableStyle.DOUBLE_BORDER)
    print(table_num_objects)
    print(
        f"Total Number of Objects: {adh.sum_attribute(sorted_num_objects, 'num_objects')}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--butler",
        type=str,
        help="Look at a particular butler bucket instead of the LFA.",
    )

    parser.add_argument("-d", "--dir", type=str, help="Add sub-dir for bucket.")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase script verbosity."
    )

    args = parser.parse_args()
    main(args)
