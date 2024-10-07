import unittest
from unittest.mock import patch, MagicMock
import gcp_cloud_security  # Replace with the actual module name

class TestGCPCloudSecurity(unittest.TestCase):

    def setUp(self):
        """Set up for GCP Cloud Security tests."""
        self.test_policy = {'policy_name': 'gcp_test_policy'}
        self.test_policies = [self.test_policy]

    def tearDown(self):
        """Clean up after each test method."""
        pass  # Add cleanup code if necessary

    @patch('gcp_cloud_security.fetch_gcp_security_policies')
    def test_fetch_policies(self, mock_fetch):
        """Test fetching GCP security policies."""
        # Mocking the response of the function
        mock_fetch.return_value = self.test_policies

        policies = gcp_cloud_security.fetch_gcp_security_policies()
        
        self.assertEqual(len(policies), 1, "Policy count mismatch")
        self.assertEqual(policies[0]['policy_name'], self.test_policy['policy_name'], "Policy name mismatch")
    
    @patch('gcp_cloud_security.sync_policies')
    def test_sync_policies_success(self, mock_sync):
        """Test successful synchronization of GCP policies."""
        mock_sync.return_value = "GCP policies synchronized successfully"

        result = gcp_cloud_security.sync_policies()
        self.assertEqual(result, "GCP policies synchronized successfully", "Synchronization message mismatch")

    @patch('gcp_cloud_security.sync_policies')
    def test_sync_policies_failure(self, mock_sync):
        """Test failure scenario for GCP policy synchronization."""
        mock_sync.side_effect = Exception("Sync failed due to network error")

        with self.assertRaises(Exception) as context:
            gcp_cloud_security.sync_policies()
        
        self.assertEqual(str(context.exception), "Sync failed due to network error", "Expected sync failure message mismatch")

    @patch('gcp_cloud_security.fetch_gcp_security_policies')
    def test_fetch_policies_empty(self, mock_fetch):
        """Test fetching policies when no policies are returned."""
        mock_fetch.return_value = []

        policies = gcp_cloud_security.fetch_gcp_security_policies()
        self.assertEqual(policies, [], "Expected empty policy list")

    @patch('gcp_cloud_security.fetch_gcp_security_policies')
    def test_fetch_policies_invalid_response(self, mock_fetch):
        """Test handling of invalid response structure."""
        mock_fetch.return_value = [{'wrong_key': 'value'}]

        with self.assertRaises(KeyError):
            # Attempting to access a non-existing key
            policies = gcp_cloud_security.fetch_gcp_security_policies()
            _ = policies[0]['policy_name']  # This should raise an error

if __name__ == '__main__':
    unittest.main()
