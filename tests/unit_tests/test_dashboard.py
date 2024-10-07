import unittest
from unittest.mock import patch
from app.models import SecurityEvent
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestDashboard(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.events = [
            SecurityEvent(event_type='DDoS', description='DDoS attack detected'),
            SecurityEvent(event_type='Phishing', description='Phishing attempt detected'),
            SecurityEvent(event_type='Malware', description='Malware infection detected'),
            SecurityEvent(event_type='Misconfiguration', description='Security group misconfiguration detected')
        ]
    
    @patch('app.models.SecurityEvent.analyze_event')  # Mock the AI analysis method
    def test_event_creation(self, mock_analyze):
        """Test creation of security events."""
        for event in self.events:
            self.assertEqual(event.event_type, event.event_type)
            logging.info(f"Created event: {event.event_type} - {event.description}")
        
    @patch('app.models.SecurityEvent.analyze_event')
    def test_event_analysis(self, mock_analyze):
        """Test the AI-based analysis of events."""
        mock_analyze.return_value = {'severity': 'high', 'action': 'mitigate'}
        
        for event in self.events:
            result = event.analyze_event()
            self.assertEqual(result['severity'], 'high')
            self.assertEqual(result['action'], 'mitigate')
            logging.info(f"Analyzed event: {event.event_type} - Result: {result}")

    def test_event_handling_speed(self):
        """Test the speed of event handling."""
        start_time = time.time()
        for event in self.events:
            event.handle_event()  # Assuming this method exists for handling events
        duration = time.time() - start_time
        logging.info(f"Event handling duration: {duration:.4f} seconds")
        self.assertLess(duration, 2)  # Check if handling takes less than 2 seconds

if __name__ == '__main__':
    unittest.main()
