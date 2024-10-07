import unittest
from unittest.mock import patch, MagicMock
import oracle_cloud_security  # Replace with the actual module name

class TestOracleCloudSecurity(unittest.TestCase):
    def setUp(self):
        """Set up for test cases. This method runs before each test."""
        self.policy_example = {'policy_name': 'oracle_test_policy', 'policy_id': '1234', 'status': 'active'}
        self.mock_policies = [self.policy_example]

    def tearDown(self):
        """Clean up after test cases. This method runs after each test."""
        pass  # Add cleanup code if necessary

    @patch('oracle_cloud_security.fetch_oracle_security_policies')
    def test_fetch_policies_success(self, mock_fetch):
        """Test fetching Oracle security policies successfully."""
        # Mocking the response of the function
        mock_fetch.return_value = self.mock_policies

        policies = oracle_cloud_security.fetch_oracle_security_policies()
        
        self.assertIsInstance(policies, list, "Expected a list of policies")
        self.assertGreater(len(policies), 0, "Expected at least one policy")
        self.assertDictEqual(policies[0], self.policy_example, "Fetched policy does not match expected policy")

    @patch('oracle_cloud_security.fetch_oracle_security_policies')
    def test_fetch_policies_empty(self, mock_fetch):
        """Test fetching Oracle security policies returns empty list."""
        # Mocking the response of the function to return an empty list
        mock_fetch.return_value = []

        policies = oracle_cloud_security.fetch_oracle_security_policies()
        
        self.assertEqual(len(policies), 0, "Expected no policies fetched")

    @patch('oracle_cloud_security.sync_policies')
    def test_sync_policies_success(self, mock_sync):
        """Test successful synchronization of Oracle security policies."""
        mock_sync.return_value = "Oracle policies synchronized successfully"

        result = oracle_cloud_security.sync_policies()
        self.assertEqual(result, "Oracle policies synchronized successfully", "Expected synchronization message did not match")

    @patch('oracle_cloud_security.sync_policies')
    def test_sync_policies_failure(self, mock_sync):
        """Test synchronization of Oracle security policies with failure."""
        mock_sync.side_effect = Exception("Synchronization failed")

        with self.assertRaises(Exception) as context:
            oracle_cloud_security.sync_policies()
        
        self.assertEqual(str(context.exception), "Synchronization failed", "Expected synchronization failure message did not match")

if __name__ == '__main__':
    unittest.main()
