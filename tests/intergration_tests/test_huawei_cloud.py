import unittest
from unittest.mock import patch
import huawei_cloud_security  # Replace with the actual module name

class TestHuaweiCloudSecurity(unittest.TestCase):
    @patch('huawei_cloud_security.fetch_huawei_security_policies')
    def test_fetch_policies(self, mock_fetch):
        # Mocking the response of the function
        mock_fetch.return_value = [{'policy_name': 'test_policy'}]

        policies = huawei_cloud_security.fetch_huawei_security_policies()
        self.assertEqual(len(policies), 1)
        self.assertEqual(policies[0]['policy_name'], 'test_policy')

    @patch('huawei_cloud_security.sync_policies')
    def test_sync_policies(self, mock_sync):
        mock_sync.return_value = "Policies synchronized successfully"

        result = huawei_cloud_security.sync_policies()
        self.assertEqual(result, "Policies synchronized successfully")

if __name__ == '__main__':
    unittest.main()
