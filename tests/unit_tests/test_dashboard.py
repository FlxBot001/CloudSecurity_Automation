import unittest
from app.models import SecurityEvent

class TestDashboard(unittest.TestCase):
    def test_event_creation(self):
        event = SecurityEvent(event_type='DDoS', description='DDoS attack detected')
        self.assertEqual(event.event_type, 'DDoS')

if __name__ == '__main__':
    unittest.main()
