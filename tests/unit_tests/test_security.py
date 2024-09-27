import unittest
from app.blueprints.security.utils import detect_threats

class TestSecurity(unittest.TestCase):
    def test_detect_threats(self):
        threats = detect_threats()
        self.assertEqual(len(threats), 1)
        self.assertEqual(threats[0]['type'], 'DDoS')

if __name__ == '__main__':
    unittest.main()
