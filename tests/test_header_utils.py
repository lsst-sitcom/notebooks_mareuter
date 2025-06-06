import logging
import unittest

import pandas as pd

import lsst.sitcom.mareuter.header_utils as hu

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class TestHeaderUtils(unittest.TestCase):
    def test_dict_from_additional(self) -> None:
        truth = {
            "imageType": "DARK",
            "groupId": "2022-04-25T21:51:16.540",
            "testType": "DARK",
            "reason": "DMTN-143",
            "program": "IntegrationTesting",
        }
        values = []
        for v in truth.values():
            if ":" in v:
                values.append(v.replace(":", r"\:"))
            else:
                values.append(v)
        data = {
            "additionalKeys": [":".join(list(truth.keys()))],
            "additionalValues": [":".join(values)],
        }
        df = pd.DataFrame(data)

        self.assertDictEqual(hu.dict_from_additional(df), truth)

    def test_get_value(self) -> None:
        empty_df = pd.DataFrame()
        self.assertIsNone(hu.get_value(empty_df, "mode"))

        data_df = pd.DataFrame({"mode": [0, 1]})
        self.assertEqual(hu.get_value(data_df, "mode"), data_df["mode"][0])
        self.assertEqual(hu.get_value(data_df, "mode", 1), data_df["mode"][1])

    def test_get_monitor_value(self) -> None:
        empty_df = pd.DataFrame()
        last_df = pd.DataFrame({"mon": [0]})
        range_df = pd.DataFrame({"mon": [2]})
        self.assertEqual(hu.get_monitor_value(last_df, empty_df, "mon", "max"), 0)
        self.assertEqual(hu.get_monitor_value(last_df, range_df, "mon", "max"), 2)
