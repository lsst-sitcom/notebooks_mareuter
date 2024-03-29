#!/usr/bin/env python
import argparse
import asyncio
import csv

from lsst_efd_client import EfdClient

from lsst.sitcom.mareuter.site_efd import get_efd


async def main(opts: argparse.Namespace) -> None:
    efd_name = get_efd()
    client = EfdClient(efd_name)
    measurements = await client.get_topics()
    cscs = []
    for measurement in measurements:
        try:
            csc = measurement.split(".")[2]
            cscs.append(csc)
        except IndexError:
            pass
    cscs_set = set(cscs)
    cscs = sorted(cscs_set)

    filename = efd_name.replace("_efd", "")
    with open(f"{filename}_cscs.csv", "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(cscs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    asyncio.run(main(args))
