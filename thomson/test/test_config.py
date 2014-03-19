import os
import unittest
from thomson.util.config.config import Config

config_path = os.path.join(os.path.dirname(Config.__file__), 'trqadrc.ini')
config = Config(config_path)

class TestConfig(unittest.TestCase):

    def test_glob(self):
        self.assertEqual(config.get('Credentials', 'Uid'), 'XXXXXXXXXX')
        self.assertEqual(config.get('Credentials', 'Pwd'), 'XXXXXXX')

if __name__ == '__main__':
    unittest.main()

