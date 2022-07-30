import os
import string
import sys
import unittest
from unittest import mock
from collections import defaultdict
from uuid import UUID
from uuid import uuid4

from shortuuid.main import decode
from shortuuid.main import encode
from shortuuid.main import get_alphabet
from shortuuid.main import random
from shortuuid.main import set_alphabet
from shortuuid.main import ShortUUID
from shortuuid.main import uuid
from shortuuid.django_fields import ShortUUIDField

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))


class LegacyShortUUIDTest(unittest.TestCase):
    def test_generation(self):
        self.assertTrue(20 < len(uuid()) < 24)
        self.assertTrue(20 < len(uuid("http://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("HTTP://www.example.com/")) < 24)
        self.assertTrue(20 < len(uuid("example.com/")) < 24)

    def test_encoding(self):
        u = UUID("{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}")
        self.assertEqual(encode(u), "CXc85b4rqinB7s5J52TRYb")

    def test_decoding(self):
        u = UUID("{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}")
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
        u = UUID("{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}")
        self.assertEqual(su.encode(u), "CXc85b4rqinB7s5J52TRYb")

    def test_decoding(self):
        su = ShortUUID()
        u = UUID("{3b1f8b40-222c-4a6e-b77e-779d5a94e21c}")
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

        base64_alphabet = (
            string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
        )

        su2 = ShortUUID(base64_alphabet)
        self.assertEqual(su2.encoded_length(), 22)

        binary_alphabet = "01"
        su3 = ShortUUID(binary_alphabet)
        self.assertEqual(su3.encoded_length(), 128)

        su4 = ShortUUID()
        self.assertEqual(su4.encoded_length(num_bytes=8), 11)


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


class EncodingEdgeCasesTest(unittest.TestCase):
    def test_decode_dict(self):
        su = ShortUUID()
        self.assertRaises(ValueError, su.encode, [])
        self.assertRaises(ValueError, su.encode, {})
        self.assertRaises(ValueError, su.decode, (2,))
        self.assertRaises(ValueError, su.encode, 42)
        self.assertRaises(ValueError, su.encode, 42.0)


class DecodingEdgeCasesTest(unittest.TestCase):
    def test_decode_dict(self):
        su = ShortUUID()
        self.assertRaises(ValueError, su.decode, [])
        self.assertRaises(ValueError, su.decode, {})
        self.assertRaises(ValueError, su.decode, (2,))
        self.assertRaises(ValueError, su.decode, 42)
        self.assertRaises(ValueError, su.decode, 42.0)


class ShortUUIDFieldTest(unittest.TestCase):
    def test_when_length_provided_use_ShortUUID_random(self):
        length, prefix, alphabet = 22, "pf", list('abcdefghijk')

        field = ShortUUIDField(length=length, prefix=prefix, alphabet=alphabet)

        self.assertEqual(field.alphabet, alphabet)
        self.assertEqual(field.length, length)
        self.assertEqual(field.prefix, prefix)
        self.assertEqual(field.max_length, length + len(prefix))
        self.assertEqual(field.default, field._generate_random)

    def test_generate_random(self):
        length, prefix, alphabet = 22, "pf", list('abcdefghijk')

        field = ShortUUIDField(length=length, prefix=prefix, alphabet=alphabet)

        random = field._generate_random()

        self.assertEqual(len(random), length + len(prefix))
        self.assertTrue(random.startswith(prefix))
        self.assert_all_characters_from_alphabet(random[len(prefix):], alphabet)

    def test_max_length_too_small_for_random(self):
        length, prefix, alphabet = 22, "pf", list('abcdefghijk')

        required_length = length + len(prefix)

        with self.assertRaises(Exception) as cm:
            ShortUUIDField(prefix=prefix, alphabet=alphabet, length=length, max_length=required_length - 1)
        self.assertEqual(str(cm.exception), f"max_length too small to fit generated random of length {required_length} (including prefix)")

    @mock.patch('shortuuid.django_fields.ShortUUID')
    def test_generate_random_actually_calls_random(self, short_uuid: mock.Mock):
        length, alphabet = 22, list('abcdefghijk')
        instance_mock = mock.MagicMock()
        short_uuid.return_value = instance_mock
        field = ShortUUIDField(length=length, alphabet=alphabet)

        field._generate_random()

        short_uuid.assert_called_once_with(alphabet=alphabet)
        instance_mock.random.assert_called_once_with(length=length)

    def test_when_no_length_provided_use_ShortUUID_uuid(self):
        prefix, alphabet = "pf", list('abcdefghijk')

        field = ShortUUIDField(prefix=prefix, alphabet=alphabet)

        self.assertEqual(field.alphabet, alphabet)
        self.assertEqual(field.length, None)
        self.assertEqual(field.prefix, prefix)
        self.assertEqual(field.max_length, len(prefix) + ShortUUID(alphabet=alphabet)._length)
        self.assertEqual(field.default, field._generate_uuid)

    def test_max_length_too_small_for_uuid(self):
        prefix, alphabet = "pf", list('abcdefghijk')

        required_length = ShortUUID(alphabet=alphabet)._length + len(prefix)

        with self.assertRaises(Exception) as cm:
            ShortUUIDField(prefix=prefix, alphabet=alphabet, max_length=required_length - 1)
        self.assertEqual(str(cm.exception), f"max_length too small to fit generated UUID of length {required_length} (including prefix)")

    @mock.patch('shortuuid.django_fields.ShortUUID')
    def test_generate_uuid_actually_calls_uuid(self, short_uuid: mock.Mock):
        length, alphabet = 22, list('abcdefghijk')
        instance_mock = mock.MagicMock()
        short_uuid.return_value = instance_mock
        field = ShortUUIDField(length=length, alphabet=alphabet)

        field._generate_uuid()

        short_uuid.assert_called_once_with(alphabet=alphabet)
        instance_mock.uuid.assert_called_once()

    def test_generate_uuid(self):
        length, prefix, alphabet = 22, "pf", list('abcdefghijk')

        field = ShortUUIDField(length=length, prefix=prefix, alphabet=alphabet)
        shortuuid = ShortUUID(alphabet=alphabet)
        required_length = len(prefix) + shortuuid._length

        generated_uuid = field._generate_uuid()

        self.assertEqual(len(generated_uuid), required_length)
        self.assert_all_characters_from_alphabet(generated_uuid[len(prefix):], alphabet)

        decoded_uuid = shortuuid.decode(generated_uuid[len(prefix):])

        self.assertEqual(decoded_uuid.__class__, UUID)

    def assert_all_characters_from_alphabet(self, test_string, alphabet):
        [self.assertTrue(c in alphabet) for c in test_string]


if __name__ == "__main__":
    unittest.main()
