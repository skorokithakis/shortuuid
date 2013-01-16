import unittest

from main import *


class ShortUUIDTest(unittest.TestCase):
    def test_everything(self):
        new_uuid = uuid()
        self.assertEqual(len(new_uuid), 22)


if __name__ == '__main__':
    unittest.main()
