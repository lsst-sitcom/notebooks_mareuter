import json
import pathlib
import typing

__all__ = ["get_csc_ackcmd_mapping"]


def get_csc_ackcmd_mapping(
    csc: str,
    xml_sal_version: str,
    save_dir: pathlib.Path = pathlib.Path("~/DATA").expanduser(),
) -> typing.Dict[int, str]:
    input_file = save_dir / f"ackcmd_translation_{xml_sal_version}.json"
    translations = json.load(input_file.open())
    return {int(k): v for k, v in translations[csc].items()}
