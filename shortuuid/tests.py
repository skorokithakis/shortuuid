import os
import string
import sys
import unittest
import pep8

from uuid import UUID, uuid4

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))
from shortuuid.main import *


class LegacyShortUUIDTest(unittest.TestCase):
    def test_generation(self):
        self.assertTrue(20 < len(uuid()) < 24)
        self.assertTrue(20 < len(uuid("http://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("HTTP://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("example.com/")) < 24)

    def test_encoding(self):
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEqual(encode(u), "VoVuUtBhZ6TvQSAYEqNdF5")

    def test_decoding(self):
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEqual(decode("VoVuUtBhZ6TvQSAYEqNdF5"), u)

    def test_alphabet(self):
        backup_alphabet = get_alphabet()

        alphabet = "01"
        set_alphabet(alphabet)
        self.assertEqual(alphabet, get_alphabet())

        set_alphabet("01010101010101")
        self.assertEqual(alphabet, get_alphabet())

        self.assertEqual(set(uuid()), set("01"))
        self.assertTrue(116 < len(uuid()) < 140)

        u = uuid4()
        self.assertEqual(u, decode(encode(u)))

        u = uuid()
        self.assertEqual(u, encode(decode(u)))

        self.assertRaises(ValueError, set_alphabet, "1")
        self.assertRaises(ValueError, set_alphabet, "1111111")

        set_alphabet(backup_alphabet)

    def test_random(self):
        self.assertEqual(len(random()), 22)
        for i in range(1, 100):
            self.assertEqual(len(random(i)), i)


class ClassShortUUIDTest(unittest.TestCase):
    def test_generation(self):
        su = ShortUUID()
        self.assertTrue(20 < len(su.uuid()) < 24)
        self.assertTrue(20 < len(su.uuid("http://www.example.com/")) < 24)
        self.assertTrue(20 < len(su.uuid("HTTP://www.example.com/")) < 24)
        self.assertTrue(20 < len(su.uuid("example.com/")) < 24)

    def test_encoding(self):
        su = ShortUUID()
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEqual(su.encode(u), "VoVuUtBhZ6TvQSAYEqNdF5")

    def test_decoding(self):
        su = ShortUUID()
        u = UUID('{12345678-1234-5678-1234-567812345678}')
        self.assertEqual(su.decode("VoVuUtBhZ6TvQSAYEqNdF5"), u)

    def test_random(self):
        su = ShortUUID()
        self.assertEqual(len(su.random()), 22)

        for i in range(1, 100):
            self.assertEqual(len(su.random(i)), i)

    def test_alphabet(self):
        alphabet = "01"
        su1 = ShortUUID(alphabet)
        su2 = ShortUUID()

        self.assertEqual(alphabet, su1.get_alphabet())

        su1.set_alphabet("01010101010101")
        self.assertEqual(alphabet, su1.get_alphabet())

        self.assertEqual(set(su1.uuid()), set("01"))
        self.assertTrue(116 < len(su1.uuid()) < 140)
        self.assertTrue(20 < len(su2.uuid()) < 24)

        u = uuid4()
        self.assertEqual(u, su1.decode(su1.encode(u)))

        u = su1.uuid()
        self.assertEqual(u, su1.encode(su1.decode(u)))

        self.assertRaises(ValueError, su1.set_alphabet, "1")
        self.assertRaises(ValueError, su1.set_alphabet, "1111111")

    def test_encoded_length(self):
        su1 = ShortUUID()
        self.assertEqual(su1.encoded_length(), 22)

        base64_alphabet = string.ascii_uppercase + \
            string.ascii_lowercase + string.digits + '+/'

        su2 = ShortUUID(base64_alphabet)
        self.assertEqual(su2.encoded_length(), 22)

        binary_alphabet = "01"
        su3 = ShortUUID(binary_alphabet)
        self.assertEqual(su3.encoded_length(), 128)

        su4 = ShortUUID()
        self.assertEqual(su4.encoded_length(num_bytes=8), 11)

    def test_pep8(self):
        pep8style = pep8.StyleGuide([['statistics', True],
                                     ['show-sources', True],
                                     ['repeat', True],
                                     ['paths', [os.path.dirname(
                                         os.path.abspath(__file__))]]],
                                    parse_argv=False,
                                    config_file=True)
        report = pep8style.check_files()
        assert report.total_errors == 0

if __name__ == '__main__':
    unittest.main()
