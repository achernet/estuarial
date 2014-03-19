import os
import unittest

import estuarial
from estuarial import Config


feldman_path = os.path.join(os.path.dirname(estuarial.__file__),'trqadrc.ini')
config = Config(feldman_path)

class TestConfig(unittest.TestCase):

    def test_glob(self):
        self.assertEqual(config.get('Credentials','Uid'),'XXXXXXXXXX')
        self.assertEqual(config.get('Credentials','Pwd'),\
                         'XXXXXXX')

if __name__ == '__main__':
    unittest.main()

