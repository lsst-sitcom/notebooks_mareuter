#!/usr/bin/env python -Xfrozen_modules=off

import argparse
import os
import pathlib
import time

from astropy.time import Time
import nbconvert
import papermill as pm
from traitlets.config import Config

DATE_FORMAT = "%Y%m%d_%H%M"
OUTPUT_DIR = pathlib.Path("reports")


def main(opts: argparse.Namespace) -> None:
    database_dir = OUTPUT_DIR / opts.database
    if not database_dir.exists():
        database_dir.mkdir()

    try:
        TOP_DIR = pathlib.Path(os.environ["NOTEBOOKS_MAREUTER_DIR"])
    except KeyError:
        TOP_DIR = pathlib.Path.cwd()
    NOTEBOOK_DIR = TOP_DIR / "notebooks" / "general" / "Diagnostics"

    start_time = Time(opts.start_time, scale="utc")
    end_time = Time(opts.end_time, scale="utc")
    start_time_fmt = start_time.strftime(DATE_FORMAT)
    end_time_fmt = end_time.strftime(DATE_FORMAT)

    output_notebook = (
        f"{opts.csc}_{opts.topic_name}_S{start_time_fmt}_E{end_time_fmt}.ipynb"
    )
    output_html = output_notebook.replace("ipynb", "html")

    report_notebook = pathlib.Path(output_notebook)
    report_output = database_dir / output_html

    pm.execute_notebook(
        NOTEBOOK_DIR / "EfdDiagnostics.ipynb",
        output_notebook,
        parameters=dict(
            csc=opts.csc,
            topic_name=opts.topic_name,
            expected_rate=opts.expected_rate,
            use_kafka=opts.use_kafka,
            efd_name=opts.database,
            start_time_str=opts.start_time,
            end_time_str=opts.end_time,
        ),
    )

    c = Config()
    c.template_file = "full"
    c.HTMLExporter.exclude_input = True
    c.HTMLExporter.exclude_output_prompt = True

    converter = nbconvert.HTMLExporter(config=c)
    body, _ = converter.from_filename(output_notebook)
    with report_output.open("w") as ofile:
        ofile.writelines(body)

    while True:
        if report_output.exists():
            report_notebook.unlink()
            break
        time.sleep(0.01)

    print(f"Saved {report_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("database", help="The EFD to get the data from")
    parser.add_argument(
        "csc", help="The CSC to run diagnostics on in for of <name>[:<index>]"
    )
    parser.add_argument(
        "topic_name", help="The topic to run diagnostics on (without lsst.sal prefix)"
    )
    parser.add_argument(
        "start_time", help="Set the query start time (TAI) in ISO8601 format"
    )
    parser.add_argument(
        "end_time", help="Set the query end time (TAI) in ISO8601 format"
    )
    parser.add_argument(
        "--expected-rate",
        default=1,
        type=float,
        help="Set the expected rate (Hz) of the topic.",
    )
    parser.add_argument(
        "--use-kafka", action="store_true", help="Generate plots for kafka."
    )

    args = parser.parse_args()

    main(args)
