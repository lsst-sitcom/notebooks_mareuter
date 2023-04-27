import logging
import unittest

import lsst.sitcom.mareuter.aws_du_helpers as adh

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class TestPlaylistUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.du_info = [
            adh.AwsDuInfo("test1", 300000, 1000),
            adh.AwsDuInfo("test2", 1000, 10),
            adh.AwsDuInfo("test3", 50000, 100),
        ]

    def test_sort_by_num_objects(self) -> None:
        sorted_info = adh.sort_by_num_objects(self.du_info)
        keys = [x.key for x in sorted_info]
        self.assertListEqual(keys, ["test1", "test3", "test2"])

    def test_sort_by_size_bytes(self) -> None:
        sorted_info = adh.sort_by_size_bytes(self.du_info)
        keys = [x.key for x in sorted_info]
        self.assertListEqual(keys, ["test1", "test3", "test2"])

    def test_sum_attribute(self) -> None:
        total_num_objects = adh.sum_attribute(self.du_info, "num_objects")
        self.assertEqual(total_num_objects, 1110)
        total_size_bytes = adh.sum_attribute(self.du_info, "size_bytes")
        self.assertEqual(total_size_bytes, 351000)

    def test_formatting(self) -> None:
        hsize = adh.get_human_size(self.du_info[0].size_bytes)
        self.assertEqual(hsize, "292.969 KiB")
        hsize = adh.get_human_size(self.du_info[1].size_bytes)
        self.assertEqual(hsize, "1000 B")
        hsize = adh.get_human_size(self.du_info[2].size_bytes)
        self.assertEqual(hsize, "48.828 KiB")
