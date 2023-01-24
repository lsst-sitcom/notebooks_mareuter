import logging
import unittest

from lsst.sitcom.mareuter.playlist_info.playlist import Playlist

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class TestPlaylistUtils(unittest.TestCase):
    def test_playlist_class(self) -> None:
        day_obs = 20220511
        seq_nums = list(range(34, 36 + 1))
        controller = "O"
        file_stem = "AT_{0}_{1}_{2:06}"
        daq_folder = "emu"

        image_name_list = [
            "AT_O_20220511_000034",
            "AT_O_20220511_000035",
            "AT_O_20220511_000036",
        ]
        image_name_string = ":".join(image_name_list)

        plist = Playlist(day_obs, seq_nums, controller, daq_folder, file_stem)

        self.assertListEqual(plist.get_image_names(), image_name_list)
        self.assertEqual(plist.get_image_names_as_string(), image_name_string)
        self.assertEqual(plist.daq_folder, daq_folder)
