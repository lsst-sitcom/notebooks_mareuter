#!/usr/bin/env python

import argparse
import json
import os
import pathlib
import sys


def main(opts):
    try:
        top_dir = os.environ["CONDA_PREFIX"]
    except KeyError:
        raise RuntimeError("CONDA_PREFIX not found! Please run setup lsst_distrib")

    try:
        opts.save_path.mkdir(755, True)
    except FileExistsError:
        pass

    version_number = ".".join([str(x) for x in sys.version_info[:2]])
    python_version = f"python{version_number}"
    idl_location = pathlib.Path(top_dir) / "lib" / python_version / "idl"
    xml_sal_version = None
    topic_mapping = {}
    for i, idl_file in enumerate(idl_location.iterdir()):
        pragma_defs = []
        csc = None
        with idl_file.open() as ifile:
            for line in ifile:
                if line.startswith("//") and i == 0:
                    idl_versions = []
                    for part in line.split():
                        if "=" in part:
                            idl_versions.append(part.split("=")[-1])
                    idl_versions.reverse()
                    xml_sal_version = "_".join(idl_versions)
                if line.startswith("module"):
                    csc = line.split()[1]
                    topic_mapping[csc] = {}
                if line.startswith("#pragma"):
                    value = line.split()[-1]
                    # Strip hash from topic
                    topic = "_".join(value.split("_")[:-1])
                    if "ackcmd" not in topic:
                        pragma_defs.append(topic)
        for j, t in enumerate(pragma_defs):
            topic_mapping[csc][j + 1] = t

    output_file = opts.save_path / f"ackcmd_translation_{xml_sal_version}.json"
    json.dump(topic_mapping, output_file.open("w"), sort_keys=True, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--save-path",
        type=pathlib.Path,
        default=pathlib.Path("~/DATA").expanduser(),
        help="Alternate location to save ackcmd translation file.",
    )

    args = parser.parse_args()

    main(args)
