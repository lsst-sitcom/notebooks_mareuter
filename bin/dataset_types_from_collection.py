#!/usr/bin/env python

import argparse

import lsst.daf.butler as dafButler


def main(opts: argparse.Namespace) -> None:
    butler = dafButler.Butler(
        opts.repo,
        collections=[f"{opts.collection}"],
    )

    for results in butler.registry.queryDatasets(...).byParentDatasetType():
        count = results.count(exact=False)
        if count:
            print(results.parentDatasetType.name, count)


if __name__ == "__main__":
    description = ["Find the Dataset types associated with a given Butler collection."]
    parser = argparse.ArgumentParser()

    parser.add_argument("repo", help="The Butler repository")
    parser.add_argument("collection", help="The collection to search.")

    args = parser.parse_args()
    main(args)
