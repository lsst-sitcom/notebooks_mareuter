import logging
import os
import unittest

from lsst.sitcom.mareuter.site_efd import get_efd

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

ENV_VAR = "LSST_SITE"


class TestSiteEfd(unittest.TestCase):
    def test_get_efd(self) -> None:
        efd_name = get_efd()
        self.assertEqual(efd_name, "usdf_efd")

        os.environ[ENV_VAR] = "summit"
        efd_name = get_efd()
        self.assertEqual(efd_name, "summit_efd")

        os.environ[ENV_VAR] = "base"
        efd_name = get_efd()
        self.assertEqual(efd_name, "base_efd")

        os.environ[ENV_VAR] = "tucson"
        efd_name = get_efd()
        self.assertEqual(efd_name, "tucson_teststand_efd")

        os.environ[ENV_VAR] = "new_place"
        with self.assertRaises(RuntimeError):
            get_efd()
