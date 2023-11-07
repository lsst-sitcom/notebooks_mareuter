#!/usr/bin/env python -Xfrozen_modules=off

import argparse
import asyncio
import os
import pathlib

import nbconvert
import papermill as pm
from traitlets.config import Config

OUTPUT_DIR = pathlib.Path("reports")


async def main(opts: argparse.Namespace) -> None:
    try:
        TOP_DIR = pathlib.Path(os.environ["NOTEBOOKS_MAREUTER_DIR"])
    except KeyError:
        TOP_DIR = pathlib.Path.cwd()
    NOTEBOOK_DIR = TOP_DIR / "notebooks" / "general" / "DomeSeeing"

    output_notebook = f"DSM_Report_{opts.date_str}.ipynb"
    output_html = output_notebook.replace("ipynb", "html")

    report_notebook = pathlib.Path(output_notebook)
    report_output = OUTPUT_DIR / output_html

    pm.execute_notebook(
        NOTEBOOK_DIR / "DSM_Report.ipynb",
        output_notebook,
        parameters=dict(
            ipath=opts.file_path,
            date_str=opts.date_str,
            csc_index=opts.csc_index,
            efd_name=opts.efd_name,
            use_old_weather=opts.use_old_weather,
        ),
    )

    c = Config()
    c.template_file = "basic"
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
        await asyncio.sleep(0)

    print(f"Saved {report_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file_path", help="Provide the file path where the data resides."
    )
    parser.add_argument(
        "date_str", help="The date string for the data to generate a report."
    )
    parser.add_argument(
        "-i",
        "--csc-index",
        type=int,
        default=1,
        help="Provide the CSC index for the data.",
    )
    parser.add_argument(
        "-e", "--efd-name", type=str, help="The EFD name to query data from."
    )
    parser.add_argument(
        "--use-old-weather",
        action="store_true",
        help="Flag to tell reporting to use old weather CSC.",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
