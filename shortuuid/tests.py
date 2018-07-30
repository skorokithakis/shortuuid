import os
import string
import sys
import unittest
import pep8
from collections import defaultdict

from uuid import UUID, uuid4

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))

from shortuuid.main import *  # noqa


class LegacyShortUUIDTest(unittest.TestCase):
    def test_generation(self):
        self.assertTrue(20 < len(uuid()) < 24)
        self.assertTrue(20 < len(uuid("http://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("HTTP://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("example.com/")) < 24)

    def test_encoding(self):
        u = UUID('{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}')
        self.assertEqual(encode(u), "CXc85b4rqinB7s5J52TRYb")

    def test_decoding(self):
        u = UUID('{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}')
        self.assertEqual(decode("CXc85b4rqinB7s5J52TRYb"), u)

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

        self.assertRaises(ValueError, lambda x: ShortUUID(x), "0")

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
        u = UUID('{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}')
        self.assertEqual(su.encode(u), "CXc85b4rqinB7s5J52TRYb")

    def test_decoding(self):
        su = ShortUUID()
        u = UUID('{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}')
        self.assertEqual(su.decode("CXc85b4rqinB7s5J52TRYb"), u)

    def test_random(self):
        su = ShortUUID()
        for i in range(1000):
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
                                    parse_argv=False)
        report = pep8style.check_files()
        assert report.total_errors == 0


class ShortUUIDPaddingTest(unittest.TestCase):
    def test_padding(self):
        su = ShortUUID()
        random_uid = uuid4()
        smallest_uid = UUID(int=0)

        encoded_random = su.encode(random_uid)
        encoded_small = su.encode(smallest_uid)

        self.assertEqual(len(encoded_random), len(encoded_small))

    def test_decoding(self):
        su = ShortUUID()
        random_uid = uuid4()
        smallest_uid = UUID(int=0)

        encoded_random = su.encode(random_uid)
        encoded_small = su.encode(smallest_uid)

        self.assertEqual(su.decode(encoded_small), smallest_uid)
        self.assertEqual(su.decode(encoded_random), random_uid)

    def test_consistency(self):
        su = ShortUUID()
        num_iterations = 1000
        uid_lengths = defaultdict(int)

        for count in range(num_iterations):
            random_uid = uuid4()
            encoded_random = su.encode(random_uid)
            uid_lengths[len(encoded_random)] += 1
            decoded_random = su.decode(encoded_random)

            self.assertEqual(random_uid, decoded_random)

        self.assertEqual(len(uid_lengths), 1)
        uid_length = next(iter(uid_lengths.keys()))  # Get the 1 value

        self.assertEqual(uid_lengths[uid_length], num_iterations)


if __name__ == '__main__':
    unittest.main()
