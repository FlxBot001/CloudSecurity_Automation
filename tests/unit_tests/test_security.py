import unittest
from unittest.mock import patch
from app.blueprints.security.utils import detect_threats

class TestSecurity(unittest.TestCase):
    
    @patch('app.blueprints.security.utils.fetch_hacking_reports')
    def test_detect_threats(self, mock_fetch_reports):
        # Mocking real-time hacking reports data
        mock_fetch_reports.return_value = [
            {'id': 1, 'type': 'DDoS', 'severity': 'high'},
            {'id': 2, 'type': 'SQL Injection', 'severity': 'medium'},
            {'id': 3, 'type': 'XSS', 'severity': 'low'},
        ]

        # Call the detect_threats function
        threats = detect_threats()

        # Check if the function returns the correct number of threats
        self.assertGreaterEqual(len(threats), 1)
        
        # Verify threat types and severity levels
        threat_types = [threat['type'] for threat in threats]
        self.assertIn('DDoS', threat_types)
        self.assertIn('SQL Injection', threat_types)
        
        # Check that all threats are classified correctly
        for threat in threats:
            self.assertIn(threat['severity'], ['low', 'medium', 'high'])

        # Additional checks can be added here based on the threat structure

if __name__ == '__main__':
    unittest.main()
