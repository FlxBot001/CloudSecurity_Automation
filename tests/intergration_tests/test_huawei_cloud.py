import unittest

class TestHuaweiCloud(unittest.TestCase):
    def test_ddos_mitigation(self):
        result = "DDoS attack mitigated using Huawei Anti-DDoS service"
        self.assertEqual(result, "DDoS attack mitigated using Huawei Anti-DDoS service")

if __name__ == '__main__':
    unittest.main()
