import logging
import os
import unittest

from lsst.sitcom.mareuter.site_lfa import get_lfa

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

ENV_VAR = "LSST_DDS_PARTITION_PREFIX"


class TestSiteLfa(unittest.TestCase):
    def test_get_lfa(self) -> None:
        os.environ[ENV_VAR] = "tucson"
        lfa = get_lfa()
        self.assertEqual(lfa.bucket, "rubinobs-lfa-tuc")
        self.assertEqual(lfa.endpoint_url, "https://s3.tu.lsst.org")
        self.assertEqual(lfa.profile, "tts")

        os.environ[ENV_VAR] = "summit"
        lfa = get_lfa()
        self.assertEqual(lfa.bucket, "rubinobs-lfa-cp")
        self.assertEqual(lfa.endpoint_url, "https://s3.cp.lsst.org")
        self.assertEqual(lfa.profile, "summit")

        os.environ[ENV_VAR] = "base"
        lfa = get_lfa()
        self.assertEqual(lfa.bucket, "rubinobs-lfa-ls")
        self.assertEqual(lfa.endpoint_url, "https://s3.ls.lsst.org")
        self.assertEqual(lfa.profile, "bts")

        os.environ[ENV_VAR] = "new_place"
        with self.assertRaises(RuntimeError):
            get_lfa()

        del os.environ[ENV_VAR]
        with self.assertRaises(RuntimeError):
            get_lfa()
