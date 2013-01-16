""" Concise UUID generation. """

import uuid as _uu

# Define our alphabet.
_ALPHABET = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
_ALPHA_LEN = len(_ALPHABET)

def encode(uuid):
    """
    Encodes a UUID into a string (LSB first) according to the alphabet
    If leftmost (MSB) bits 0, string might be shorter
    """
    unique_id = uuid.int
    output = ""
    while unique_id:
        unique_id, digit = divmod(unique_id, _ALPHA_LEN)
        output += _ALPHABET[digit]
    return output

def decode(string):
    """
    Decodes a string according to the current alphabet into a UUID
    Raises ValueError when encountering illegal characters or too long string
    If string too short, fills leftmost (MSB) bits with 0.
    """
    number = 0
    for char in string[::-1]:
        number = number * _ALPHA_LEN + _ALPHABET.index(char)
    return _uu.UUID(int=number)

def uuid(name=None):
    """
    Generate and return a UUID.

    If the name parameter is provided, set the namespace to the provided
    name and generate a UUID.
    """
    # If no name is given, generate a random UUID.
    if name is None:
        uuid = _uu.uuid4()
    elif not "http" in name:
        uuid = _uu.uuid5(_uu.NAMESPACE_DNS, name)
    else:
        uuid = _uu.uuid5(_uu.NAMESPACE_URL, name)
    return encode(uuid)

def get_alphabet():
    """Return the current alphabet used for new UUIDs."""
    return ''.join(_ALPHABET)

def set_alphabet(alphabet):
    """Set the alphabet to be used for new UUIDs."""
    global _ALPHABET, _ALPHA_LEN

    # Turn the alphabet into a set and sort it to prevent duplicates
    # and ensure reproducibility.
    new_alphabet = list(sorted(set(alphabet)))
    if len(new_alphabet) > 1:
        _ALPHABET = new_alphabet
        _ALPHA_LEN = len(_ALPHABET)
    else:
        raise ValueError("Alphabet with more than one unique symbols required.")
