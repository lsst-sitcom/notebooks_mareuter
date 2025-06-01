#!/usr/bin/env python

import argparse
import json
import pathlib

from lsst.ts.xml import __version__, subsystems
from lsst.ts.xml.component_info import ComponentInfo


def main(opts: argparse.Namespace) -> None:
    try:
        opts.save_path.mkdir(755, True)
    except FileExistsError:
        pass

    topic_mapping: dict[str, dict[int, str]] = {}
    for csc in set(subsystems):
        topic_mapping[csc] = {}
        c = ComponentInfo(csc, "testit")
        schemas = c.make_avro_schema_dict()

        topics = []
        for topic, schema_dict in schemas.items():
            if "evt_" in topic:
                topic = topic.replace("evt_", "logevent_")
            if "tel_" in topic:
                topic = topic.replace("tel_", "")
            if "cmd_" in topic:
                topic = topic.replace("cmd_", "command_")
            if "ack_" in topic:
                continue
            topics.append(topic)

        topics = sorted(topics)
        for j, t in enumerate(topics):
            topic_mapping[csc][j + 1] = t

    output_file = opts.save_path / f"ackcmd_translation_{__version__}.json"
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
