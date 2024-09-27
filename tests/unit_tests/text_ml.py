import unittest
from ml.train import train_model

class TestML(unittest.TestCase):
    def test_train_model(self):
        model = train_model({'data': 'sample_data'})
        self.assertEqual(model, 'trained_model')

if __name__ == '__main__':
    unittest.main()
