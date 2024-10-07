import unittest
from unittest.mock import patch
import azure_cloud_security  # Replace with the actual module name
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for testing
TEST_POLICY_NAME = 'azure_test_policy'
TEST_SUCCESS_MESSAGE = 'Azure policies synchronized successfully'

class TestAzureCloudSecurity(unittest.TestCase):

    def setUp(self):
        """Set up test dependencies and variables."""
        self.mock_fetch = patch('azure_cloud_security.fetch_azure_security_policies').start()
        self.mock_sync = patch('azure_cloud_security.sync_policies').start()

    def tearDown(self):
        """Stop all patches after each test."""
        patch.stopall()

    def test_fetch_policies_success(self):
        """Test fetching Azure security policies successfully."""
        self.mock_fetch.return_value = [{'policy_name': TEST_POLICY_NAME}]
        
        policies = azure_cloud_security.fetch_azure_security_policies()
        logger.info("Fetched Policies: %s", policies)

        self.assertEqual(len(policies), 1)
        self.assertEqual(policies[0]['policy_name'], TEST_POLICY_NAME)

    def test_sync_policies_success(self):
        """Test successful synchronization of Azure policies."""
        self.mock_sync.return_value = TEST_SUCCESS_MESSAGE
        
        result = azure_cloud_security.sync_policies()
        logger.info("Sync Result: %s", result)

        self.assertEqual(result, TEST_SUCCESS_MESSAGE)

    def test_sync_policies_failure(self):
        """Test handling of synchronization failures."""
        self.mock_sync.side_effect = Exception("Synchronization failed")
        
        with self.assertRaises(Exception) as context:
            azure_cloud_security.sync_policies()
        
        logger.error("An error occurred during sync: %s", context.exception)

    def test_fetch_policies_empty(self):
        """Test fetching policies when no policies exist."""
        self.mock_fetch.return_value = []
        
        policies = azure_cloud_security.fetch_azure_security_policies()
        logger.info("Fetched Policies: %s", policies)

        self.assertEqual(policies, [])

if __name__ == '__main__':
    unittest.main()
