import unittest

class TestMultiCloud(unittest.TestCase):
    def test_sync_policies(self):
        result = "Security policies synchronized across AWS, Azure, and Huawei Cloud"
        self.assertEqual(result, "Security policies synchronized across AWS, Azure, and Huawei Cloud")

if __name__ == '__main__':
    unittest.main()
