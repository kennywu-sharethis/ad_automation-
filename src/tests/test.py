import unittest
from src.util.download_util import verify_file_size

class MyTestCase(unittest.TestCase):
    def test_verify_file_size(self):
        self.assertTrue(verify_file_size("/Users/kennywu/Documents/adsupport_pipeline/src/tests/test/testfile.csv", 500000))
        self.assertFalse(verify_file_size("/Users/kennywu/Documents/adsupport_pipeline/src/tests/test/testfile.csv", 800000))


if __name__ == '__main__':
    unittest.main()
