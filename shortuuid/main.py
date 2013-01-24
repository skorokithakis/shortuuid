""" Concise UUID generation. """

import uuid as _uu


class ShortUUID(object):
    def __init__(self, alphabet=None):
        if alphabet is None:
            # Define our alphabet.
            self._alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
            self._alpha_len = len(self._alphabet)

    def encode(self, uuid):
        """
        Encodes a UUID into a string (LSB first) according to the alphabet
        If leftmost (MSB) bits 0, string might be shorter
        """
        unique_id = uuid.int
        output = ""
        while unique_id:
            unique_id, digit = divmod(unique_id, self._alpha_len)
            output += self._alphabet[digit]
        return output

    def decode(self, string):
        """
        Decodes a string according to the current alphabet into a UUID
        Raises ValueError when encountering illegal characters or too long string
        If string too short, fills leftmost (MSB) bits with 0.
        """
        number = 0
        for char in string[::-1]:
            number = number * self._alpha_len + self._alphabet.index(char)
        return _uu.UUID(int=number)

    def uuid(self, name=None):
        """
        Generate and return a UUID.

        If the name parameter is provided, set the namespace to the provided
        name and generate a UUID.
        """
        # If no name is given, generate a random UUID.
        if name is None:
            uuid = _uu.uuid4()
        elif not "http" in name.lower():
            uuid = _uu.uuid5(_uu.NAMESPACE_DNS, name)
        else:
            uuid = _uu.uuid5(_uu.NAMESPACE_URL, name)
        return self.encode(uuid)

    def get_alphabet(self):
        """Return the current alphabet used for new UUIDs."""
        return ''.join(self._alphabet)

    def set_alphabet(self, alphabet):
        """Set the alphabet to be used for new UUIDs."""

        # Turn the alphabet into a set and sort it to prevent duplicates
        # and ensure reproducibility.
        new_alphabet = list(sorted(set(alphabet)))
        if len(new_alphabet) > 1:
            self._alphabet = new_alphabet
            self._alpha_len = len(self._alphabet)
        else:
            raise ValueError("Alphabet with more than one unique symbols required.")

# For backwards compatibility
_global_instance = ShortUUID()
encode = _global_instance.encode
decode = _global_instance.decode
uuid = _global_instance.uuid
get_alphabet = _global_instance.get_alphabet
set_alphabet = _global_instance.set_alphabet
