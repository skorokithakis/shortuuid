import unittest

from uuid import UUID, uuid4
from main import *


class ShortUUIDTest(unittest.TestCase):
    def test_generation(self):
        self.assertEqual(len(uuid()), 22)
        self.assertEqual(len(uuid("http://www.example.com/")), 22)
        self.assertEqual(len(uuid("HTTP://www.example.com/")), 22)
        self.assertEqual(len(uuid("example.com")), 22)

    def test_encoding(self):
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEquals(encode(u), "VoVuUtBhZ6TvQSAYEqNdF5")

    def test_decoding(self):
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEquals(decode("VoVuUtBhZ6TvQSAYEqNdF5"), u)

    def test_alphabet(self):
        backup_alphabet = get_alphabet()

        alphabet = "01"
        set_alphabet(alphabet)
        self.assertEquals(alphabet, get_alphabet())

        set_alphabet("01010101010101")
        self.assertEquals(alphabet, get_alphabet())

        self.assertEquals(set(uuid()), set("01"))
        self.assertTrue(120 < len(uuid()) < 136)

        u = uuid4()
        self.assertEquals(u, decode(encode(u)))

        u = uuid()
        self.assertEquals(u, encode(decode(u)))

        self.assertRaises(ValueError, set_alphabet, "1")
        self.assertRaises(ValueError, set_alphabet, "1111111")

        set_alphabet(backup_alphabet)


if __name__ == '__main__':
    unittest.main()
